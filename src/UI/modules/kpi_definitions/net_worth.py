import streamlit as st
import json
from collections import defaultdict
from modules.mcp_tools import call_mcp_tool, extract_and_clean_json
import pandas as pd

# --- Function to Fetch Cleaned Net Worth Data ---
def fetch_cleaned_net_worth(session_id: str, base_url: str) -> dict | None:
    tool = "fetch_net_worth"
    result = call_mcp_tool(tool, session_id, base_url)
    if result:
        return extract_and_clean_json(result)
    return None

# --- Session ID and Base URL ---
session_id = st.session_state.get("session_id")
base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

# --- Function to Extract Net Worth KPIs ---
def extract_net_worth_kpis(cleaned_data: dict) -> dict:
    try:
        total_assets = 0.0
        total_liabilities = 0.0
        total_epf = 0.0
        total_mf = 0.0

        # Extract Asset Values from cleaned data
        for asset in cleaned_data.get("netWorthResponse", {}).get("assetValues", []):
            value = asset.get("value", {}).get("units", 0.0)
            if "ASSET_TYPE_EP" in asset.get("netWorthAttribute", "").upper():
                total_epf += float(value)
            elif "ASSET_TYPE_MF" in asset.get("netWorthAttribute", "").upper():
                total_mf += float(value)

        # For Total Net Worth Calculation
        total_net_worth = float(cleaned_data.get("netWorthResponse", {}).get("totalNetWorthValue", {}).get("units", 0))

        # Basic benchmarks for each KPI
        return {
            "TOTAL_NET_WORTH": {
                "value": total_net_worth,
                "change": "",
                "unit": "₹",
                "icon": "💰",
                "benchmark": basic_benchmark("TOTAL_NET_WORTH", total_net_worth),
            },
            "ASSET_ALLOCATION_EPFS": {
                "value": total_epf / total_assets if total_assets else 0,
                "change": "",
                "unit": "%",
                "icon": "📊",
                "benchmark": basic_benchmark("ASSET_ALLOCATION_EPFS", total_epf / total_assets if total_assets else 0),
            },
            "ASSET_ALLOCATION_MFS": {
                "value": total_mf / total_assets if total_assets else 0,
                "change": "",
                "unit": "%",
                "icon": "📈",
                "benchmark": basic_benchmark("ASSET_ALLOCATION_MFS", total_mf / total_assets if total_assets else 0),
            },
            "LIABILITY_OTHER_LOANS": {
                "value": total_liabilities / total_assets if total_assets else 0,
                "change": "",
                "unit": "%",
                "icon": "💳",
                "benchmark": basic_benchmark("LIABILITY_OTHER_LOANS", total_liabilities / total_assets if total_assets else 0),
            },
        }
    except Exception as e:
        return {"ERROR": {"value": str(e), "change": ""}}

def basic_benchmark(kpi_name: str, value: float) -> str:
    """
    Return basic benchmark for KPIs based on common standards.
    :param kpi_name: The name of the KPI.
    :param value: The value of the KPI to classify.
    :return: Classification status (e.g., 'Good', 'Average', 'Poor').
    """
    # Define benchmarks based on common standards
    benchmarks = {
        "TOTAL_NET_WORTH": {
            "good": 1000000,  # ₹1M or more is 'Good'
            "average": 500000,  # ₹500K or more is 'Average'
            "poor": 0,  # Less than ₹500K is 'Poor'
        },
        "ASSET_ALLOCATION_EPFS": {
            "good": 40,  # 40% or more in EPF is 'Good'
            "average": 20,  # 20-40% is 'Average'
            "poor": 0,  # Less than 20% is 'Poor'
        },
        "ASSET_ALLOCATION_MFS": {
            "good": 30,  # 30% or more in MF is 'Good'
            "average": 15,  # 15-30% is 'Average'
            "poor": 0,  # Less than 15% is 'Poor'
        },
        "LIABILITY_OTHER_LOANS": {
            "good": 10,  # 10% or less liability is 'Good'
            "average": 20,  # 10-20% is 'Average'
            "poor": 30,  # More than 20% is 'Poor'
        },
    }

    # Return static benchmark status based on thresholds
    if kpi_name in benchmarks:
        thresholds = benchmarks[kpi_name]
        if value >= thresholds["good"]:
            return "Good"
        elif value >= thresholds["average"]:
            return "Average"
        else:
            return "Poor"
    return "Unknown"


# --- Function to Get Selected Net Worth KPIs for UI Display ---
def get_selected_net_worth_kpis(cleaned_data: dict) -> dict:
    # Call the internal KPI extraction function
    kpis = extract_net_worth_kpis(cleaned_data)

    # Return the KPIs to display
    return {
        "TOTAL_NET_WORTH": kpis["TOTAL_NET_WORTH"],
        "ASSET_ALLOCATION_EPFS": kpis["ASSET_ALLOCATION_EPFS"],
        "ASSET_ALLOCATION_MFS": kpis["ASSET_ALLOCATION_MFS"],
        "LIABILITY_OTHER_LOANS": kpis["LIABILITY_OTHER_LOANS"],
    }

# --- Fetch and Display KPIs ---
cleaned_net_worth_data = fetch_cleaned_net_worth(session_id, base_url)

if cleaned_net_worth_data:
    net_worth_kpis = get_selected_net_worth_kpis(cleaned_net_worth_data)

    # Display Net Worth KPIs in Streamlit (commented out for now)
    # st.subheader("Net Worth KPIs")
    # st.json(net_worth_kpis)  # Show KPIs in JSON format
else:
    cleaned_net_worth_data=0





# # modules/kpi_definitions/net_worth.py
# # Contains KPI calculations related to net worth.

# def calculate_net_worth():
#     """
#     Placeholder function to calculate the user's net worth.
#     In a real app, this would read multiple data files (bank, investments, liabilities).

#     Returns a hardcoded value for the prototype.
#     """
#     # In the future, you could use json here:
#     # import json
#     # with open('data/USER_ALEX/net_worth.json', 'r') as f:
#     #     data = json.load(f)
#     # value = data['net_worth']
#     # change = value - data['history'][0]['net_worth']
#     return {'value': 250000, 'change': 5000.0}
