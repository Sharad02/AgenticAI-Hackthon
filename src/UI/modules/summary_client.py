
import json
from vertex_chat import get_vertex_response
from modules.mcp_tools import call_mcp_tool
import streamlit as st

def fetch_financial_data(tools, session_id, base_url):
    """Fetch data from multiple MCP tools and return a combined result."""
    combined_data = {}
    for tool in tools:
        result = None
        try:
            result = call_mcp_tool(tool, session_id, base_url)
            if isinstance(result, str):
                result = json.loads(result)
        except Exception as e:
            st.error(f"❌ Error fetching {tool}: {e}")
        combined_data[tool] = result
    return combined_data

def generate_summary_prompt(combined_data):
    """Generate the prompt for the LLM using the fetched financial data."""
    return f"""
You are a personal financial assistant.

Using the following structured financial data, write a short summary of the user's overall financial health in 5 bulletin points. Highlight key strengths (e.g., good net worth, positive investments), weaknesses (e.g., loans, credit score issues), and suggest actions (e.g., reduce EMI, increase savings).
**Formatting Instructions:**
- Use `<span style="color: #F2CB5A;">...</span>` to highlight **positive** numbers, strengths, and key terms.
- Use `<span style="color: #FF6B6B;">...</span>` to highlight **negative** numbers, weaknesses, or areas for improvement.
- Add `<br>` after each point.
- Do not include any other message like 'Here is your summary'.
- Maximum length should be 500 characters.
Financial Data:
{json.dumps(combined_data, indent=2)}
"""

def get_financial_summary():
    """Fetch data from MCP tools and generate a financial health summary using Gemini."""
    session_id = st.session_state.get("session_id")
    base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
    tools = ["fetch_net_worth", "fetch_mf_transactions", "fetch_stock_transactions", "fetch_credit_report"]
    
    # Fetch the combined data from MCP tools
    combined_data = fetch_financial_data(tools, session_id, base_url)

    # Create summary prompt for LLM
    prompt = generate_summary_prompt(combined_data)
    
    try:
        # Get the summary from Gemini
        summary = get_vertex_response(prompt)
        return summary.strip()
    except Exception as e:
        return f"⚠️ Error generating summary: {e}"




# ###########################################  WORKING VERSION 1 #######################################
# import json
# from vertex_chat import get_vertex_response
# from modules.mcp_tools import call_mcp_tool
# import streamlit as st

# def get_financial_summary():
#     """Fetch data from MCP tools and generate a financial health summary using Gemini."""

#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     tools = ["fetch_net_worth", "fetch_mf_transactions", "fetch_stock_transactions", "fetch_credit_report"]

#     combined_data = {}

#     for tool in tools:
#         try:
#             result = call_mcp_tool(tool, session_id, base_url)
#             if isinstance(result, str):
#                 result = json.loads(result)
#             combined_data[tool] = result
#         except Exception as e:
#             combined_data[tool] = f"Error fetching {tool}: {str(e)}"



#     # Create summary prompt for LLM
#     prompt = f"""
# You are a personal financial assistant.

# Using the following structured financial data, write a short summary of the user's overall financial health in 5 bulletin points. Highlight key strengths (e.g., good net worth, positive investments), weaknesses (e.g., loans, credit score issues), and suggest actions (e.g., reduce EMI, increase savings).
# **Formatting Instructions:**
# - Use `<span style="color: #F2CB5A;">...</span>` to highlight **positive** numbers, strengths, and key terms.
# - Use `<span style="color: #FF6B6B;">...</span>` to highlight **negative** numbers, weaknesses, or areas for improvement.
# - Add `<br>` after each point.
# - Do not include any other message like 'Here is your summary'.
# - Maximum length should be 500 characters.
# Financial Data:
# {json.dumps(combined_data, indent=2)}

# """

#     try:
#         summary = get_vertex_response(prompt)
#         return summary.strip()
#     except Exception as e:
#         return f"⚠️ Error generating summary: {e}"
