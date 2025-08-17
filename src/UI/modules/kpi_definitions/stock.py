import streamlit as st
import json
from collections import defaultdict
from modules.mcp_tools import call_mcp_tool, extract_and_clean_json
import pandas as pd

# --- Function to Fetch Cleaned Stock Data ---
def fetch_cleaned_stock_data(session_id: str, base_url: str) -> dict | None:
    tool = "fetch_stock_transactions"
    result = call_mcp_tool(tool, session_id, base_url)
    if result:
        return extract_and_clean_json(result)
    return None

# --- Session ID and Base URL ---
session_id = st.session_state.get("session_id")
base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

# --- Function to Extract Stock KPIs ---
def extract_stock_kpis(cleaned_data: dict) -> dict:
    try:
        total_investment = 0.0
        total_sell_value = 0.0
        total_bonus_quantity = 0
        total_split_quantity = 0

        # Extract Stock Values from cleaned data
        for stock in cleaned_data.get("stockTransactions", []):
            for txn in stock.get("txns", []):
                txn_type = txn[0]
                quantity = txn[2]
                nav_value = txn[3] if len(txn) > 3 else 0.0  # Handle navValue being optional

                if txn_type == 1:  # BUY
                    total_investment += quantity * nav_value if nav_value else 0
                elif txn_type == 2:  # SELL
                    total_sell_value += quantity * nav_value if nav_value else 0
                elif txn_type == 3:  # BONUS
                    total_bonus_quantity += quantity
                elif txn_type == 4:  # SPLIT
                    total_split_quantity += quantity

        # Basic benchmarks for each KPI
        return {
            "TOTAL_INVESTMENT": {
                "value": total_investment,
                "change": "",
                "unit": "₹",
                "icon": "💰",
                "benchmark": basic_benchmark("TOTAL_INVESTMENT", total_investment),
            },
            "TOTAL_SELL_VALUE": {
                "value": total_sell_value,
                "change": "",
                "unit": "₹",
                "icon": "📈",
                "benchmark": basic_benchmark("TOTAL_SELL_VALUE", total_sell_value),
            },
            "TOTAL_BONUS_QUANTITY": {
                "value": total_bonus_quantity,
                "change": "",
                "unit": "Shares",
                "icon": "🎁",
                "benchmark": basic_benchmark("TOTAL_BONUS_QUANTITY", total_bonus_quantity),
            },
            "TOTAL_SPLIT_QUANTITY": {
                "value": total_split_quantity,
                "change": "",
                "unit": "Shares",
                "icon": "🔁",
                "benchmark": basic_benchmark("TOTAL_SPLIT_QUANTITY", total_split_quantity),
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
        "TOTAL_INVESTMENT": {
            "good": 50000,  # ₹50K or more is 'Good'
            "average": 20000,  # ₹20K or more is 'Average'
            "poor": 0,  # Less than ₹20K is 'Poor'
        },
        "TOTAL_SELL_VALUE": {
            "good": 50000,  # ₹50K or more is 'Good'
            "average": 20000,  # ₹20K or more is 'Average'
            "poor": 0,  # Less than ₹20K is 'Poor'
        },
        "TOTAL_BONUS_QUANTITY": {
            "good": 100,  # 100 shares or more is 'Good'
            "average": 50,  # 50-100 shares is 'Average'
            "poor": 0,  # Less than 50 shares is 'Poor'
        },
        "TOTAL_SPLIT_QUANTITY": {
            "good": 100,  # 100 shares or more is 'Good'
            "average": 50,  # 50-100 shares is 'Average'
            "poor": 0,  # Less than 50 shares is 'Poor'
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

# --- Function to Get Selected Stock KPIs for UI Display ---
def get_selected_stock_kpis(cleaned_data: dict) -> dict:
    # Call the internal KPI extraction function
    kpis = extract_stock_kpis(cleaned_data)

    # Return the KPIs to display
    return {
        "TOTAL_INVESTMENT": kpis["TOTAL_INVESTMENT"],
        "TOTAL_SELL_VALUE": kpis["TOTAL_SELL_VALUE"],
        "TOTAL_BONUS_QUANTITY": kpis["TOTAL_BONUS_QUANTITY"],
        "TOTAL_SPLIT_QUANTITY": kpis["TOTAL_SPLIT_QUANTITY"],
    }

# --- Fetch and Display KPIs ---
cleaned_stock_data = fetch_cleaned_stock_data(session_id, base_url)

if cleaned_stock_data:
    stock_kpis = get_selected_stock_kpis(cleaned_stock_data)

    # Display Stock KPIs in Streamlit (commented out for now)
    # st.subheader("Stock KPIs")
    # st.json(stock_kpis)  # Show KPIs in JSON format
else:
    cleaned_stock_data=0