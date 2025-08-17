import json
import os
import streamlit as st
from vertex_chat import get_vertex_response  # Assuming this is correctly imported and works
from modules.kpi_definitions.strategic_kpi import strategic_data
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel
import re  # Import the re module for regular expressions

session_id = st.session_state.get("session_id")
base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nirpu/Desktop/Agent_AI/UI/agentic-ai-466415-5a1005031578.json"

# # Initialize Vertex AI
# aiplatform.init(project="agentic-ai-466415", location="us-central1")

# # Load Gemini model
# model = GenerativeModel("gemini-2.0-flash")

# Initialize a global variable to store the kpi_list
kpi_list = []

def get_top_kpis_with_summary(user_id):
    """
    Uses Gemini AI to return a summary and the top 4 KPIs for the user based on financial health,
    including their corresponding values.

    Returns:
        dict: {
            "summary": str,
            "recommended_kpis": list[str],
            "kpi_values": dict[str, any]
        }
    """
    print(f"🎯 Analyzing financial KPIs for user {user_id}...")

    strategic_data_dict = strategic_data  # Not calling, using the dict directly

    # Flatten and format KPI values for the prompt
    all_kpis = {}
    for category in strategic_data_dict:
        for kpi_name, kpi_info in strategic_data_dict[category].items():
            if isinstance(kpi_info, dict) and "value" in kpi_info:
                all_kpis[kpi_name] = kpi_info["value"]
            else:
                all_kpis[kpi_name] = kpi_info  # Fallback if 'value' key is missing or not a dict

    formatted_kpis = "\n".join([f"- {k}: {v}" for k, v in all_kpis.items()])

    prompt = f"""
       "" You are a finance analyst, 
        Analyze the provided financial KPIs. Identify the top 4 most significant indicators from the given data and if there is an ERROR in the data fill in with another KPI"

        Format:
        Summary: <your summary>
        KPIs: ["KPI_1", "KPI_2", "KPI_3", "KPI_4"]

        Data:
        {formatted_kpis}
    """

    try:
        response = get_vertex_response(prompt)  # Assuming get_vertex_response returns a string
        raw_text = response.strip()

        summary_section = ""
        kpi_list_temp = []  # Temporary list to hold KPIs

        if "KPIs:" in raw_text:
            parts = raw_text.split("KPIs:", 1)  # Split only on the first occurrence
            summary_section = parts[0].replace("Summary:", "").strip()

            # Use regex to extract the JSON array part
            kpi_json_match = re.search(r'\[.*?\]', parts[1].strip())
            if kpi_json_match:
                kpi_list_str = kpi_json_match.group(0)
                kpi_list_temp = json.loads(kpi_list_str)
            else:
                raise ValueError("❌ No valid JSON array found for KPIs in Gemini response.")

        if not isinstance(kpi_list_temp, list) or len(kpi_list_temp) != 4:
            raise ValueError(f"❌ Invalid KPI format or count received from Gemini. Expected 4 KPIs, got {len(kpi_list_temp) if isinstance(kpi_list_temp, list) else 'N/A'}.")

        # Storing the kpi_list globally
        global kpi_list
        kpi_list = kpi_list_temp

        print("✅ AI Summary:", summary_section)
        print("✅ AI Recommended KPIs:", kpi_list)

        kpi_values = {
            kpi: all_kpis.get(kpi, "N/A") for kpi in kpi_list
        }

        return {
            "summary": summary_section,
            "recommended_kpis": kpi_list,
            "kpi_values": kpi_values
        }

    except Exception as e:
        print(f"❌ Gemini AI Parsing Error: {e}")
        return {
            "summary": "Default summary: AI failed to parse. Fallback used.",
            "recommended_kpis": [],
            "kpi_values": {}
        }


# # modules/ai_selector.py
# # This module simulates the AI agent's decision-making process.

# def get_recommended_kpis(user_id: str) -> list:
#     """
#     Simulates an AI agent analyzing user data and recommending KPIs.

#     For this prototype, it returns a hardcoded list of KPIs.
#     In a real application, this function would contain complex logic to
#     analyze the user's financial data (from CSVs, APIs, etc.) and
#     dynamically select the most relevant KPIs to display.

#     Args:
#         user_id (str): The ID of the user.

#     Returns:
#         list: A list of recommended KPI names (as strings).
#     """
#     print(f"AI Selector: Analyzing data for {user_id}...")

#     # For the hackathon prototype, we return a fixed list.
#     # This demonstrates the structure of the application.
#     recommendations = [
#         'NET_WORTH',
#         'PORTFOLIO_PERFORMANCE',
#         'SAVINGS_RATE',
#         'CREDIT_SCORE'
#     ]

#     print(f"AI Selector: Recommending KPIs: {recommendations}")
#     return recommendations
