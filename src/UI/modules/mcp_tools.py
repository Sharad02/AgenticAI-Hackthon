############################ NIRPU
import requests
import json
import streamlit as st
import os
import pandas as pd
import ace_tools_open as tools

# === List of MCP Tool Endpoints ===
TOOLS = [
    "fetch_net_worth",
    "fetch_credit_report",
    "fetch_epf_details",
    "fetch_bank_transactions",
    "fetch_mf_transactions",
    "fetch_stock_transactions"
]

# === Function to Call MCP Tool ===
def call_mcp_tool(tool_name: str, session_id: str, base_url: str) -> dict | None:
    try:
        url = f"{base_url}/mcp/stream"
        params = {"toolName": tool_name, "sessionId": session_id}
        resp = requests.get(url, params=params, timeout=10)

        if "application/json" in resp.headers.get("Content-Type", ""):
            return resp.json()
        return json.loads(resp.text)
    except Exception as e:
        st.error(f"❌ Failed to fetch {tool_name}: {e}")
        return None

# === Function to Clean Nested Escaped JSON in "text" ===
def extract_and_clean_json(tool_response: dict) -> dict | None:
    try:
        if "result" in tool_response and isinstance(tool_response["result"], dict):
            if "text" in tool_response["result"]:
                return json.loads(tool_response["result"]["text"])
        return tool_response
    except Exception as e:
        st.warning(f"⚠️ Failed to clean nested JSON: {e}")
        return tool_response

# === Function to Compute Banking KPIs ===
from typing import Dict

def extract_selected_banking_kpis(bank_transactions_data: dict) -> Dict[str, float]:
    """
    Extracts key banking KPIs from MCP bank transaction data.

    Args:
        bank_transactions_data (dict): Raw data from the 'fetch_bank_transactions' tool.

    Returns:
        dict: A dictionary containing the following KPIs:
            - Net Cash Flow
            - Total Credit Amount
            - Total Debit Amount
            - Average Transaction Amount
            - UPI Transaction Dominance (%)
    """
    transactions = []
    for account in bank_transactions_data.get("bankTransactions", []):
        for txn in account.get("txns", []):
            transactions.append(txn)

    total_credit = 0.0
    total_debit = 0.0
    total_amount = 0.0
    upi_count = 0
    total_txn_count = 0

    for txn in transactions:
        try:
            amount = float(txn[0])
            narration = txn[1]
            txn_type = int(txn[3])  # 1 = CREDIT, 2 = DEBIT

            total_txn_count += 1
            total_amount += abs(amount)

            if txn_type == 1:
                total_credit += amount
            elif txn_type == 2:
                total_debit += amount

            if "UPI" in narration.upper():
                upi_count += 1
        except Exception as e:
            # Optionally log this if needed
            continue

    net_cash_flow = total_credit - total_debit
    avg_txn_amount = total_amount / total_txn_count if total_txn_count else 0
    upi_dominance = (upi_count / total_txn_count * 100) if total_txn_count else 0

    return {
        "Net Cash Flow": round(net_cash_flow, 2),
        "Total Credit Amount": round(total_credit, 2),
        "Total Debit Amount": round(total_debit, 2),
        "Average Transaction Amount": round(avg_txn_amount, 2),
        "UPI Transaction Dominance (%)": round(upi_dominance, 2)
    }

# 1. Fetching Credit Report
def fetch_cleaned_credit_report(session_id: str, base_url: str) -> dict | None:
    tool = "fetch_credit_report"
    result = call_mcp_tool(tool, session_id, base_url)
    if result:
        return extract_and_clean_json(result)
    return None


def load_all_tools(session_id: str, base_url: str):
    if "fetched_data" not in st.session_state:
        st.session_state.fetched_data = {}

    output_dir = "Data/all_tools_cleaned"
    os.makedirs(output_dir, exist_ok=True)

    for tool in TOOLS:
        result = call_mcp_tool(tool, session_id, base_url)
        if result:
            cleaned = extract_and_clean_json(result)
            st.session_state.fetched_data[tool] = cleaned

            output_path = os.path.join(output_dir, f"{tool}.json")
            with open(output_path, "w") as f:
                json.dump(cleaned, f, indent=2)

################################################## WORKING CODE#######################################
# """
# This module provides utility functions to interact with the MCP server and
# retrieve financial data for a given user session.

# Functions:
# - call_mcp_tool(): Fetches individual tool data from the MCP API
# - load_all_tools(): Loads all predefined tools and caches results in session state
# """


# """
# MCP Tool Fetcher

# This module interacts with the MCP server to retrieve financial data
# like net worth, credit reports, EPF details, and transactions.
# """

# import requests
# import json
# import streamlit as st

# # Tool names to load from MCP
# TOOLS = [
#     "fetch_net_worth",
#     "fetch_credit_report",
#     "fetch_epf_details",
#     "fetch_bank_transactions",
#     "fetch_mf_transactions",
#     "fetch_stock_transactions"
# ]

# def call_mcp_tool(tool_name: str, session_id: str, base_url: str) -> dict | None:
#     """
#     Fetches data for a specific financial tool from the MCP server.

#     Args:
#         tool_name (str): The MCP tool to call (e.g., 'fetch_net_worth').
#         session_id (str): The user session ID used for authentication.
#         base_url (str): The base URL of the MCP server.

#     Returns:
#         dict | None: Parsed JSON response from the tool if successful, otherwise None.
#     """
#     try:
#         url = f"{base_url}/mcp/stream"
#         params = {"toolName": tool_name, "sessionId": session_id}
#         resp = requests.get(url, params=params, timeout=10)

#         if "application/json" in resp.headers.get("Content-Type", ""):
#             return resp.json()
#         return json.loads(resp.text)
#     except Exception as e:
#         st.error(f"❌ Failed to fetch {tool_name}: {e}")
#         return None

# def load_all_tools(session_id: str, base_url: str):
#     """
#     Calls a set of predefined MCP tools and stores the results in Streamlit's session state.

#     The fetched data is stored in:
#         st.session_state["fetched_data"]

#     Args:
#         session_id (str): The user session ID.
#         base_url (str): The MCP server base URL.
#     """
#     if "fetched_data" not in st.session_state:
#         st.session_state.fetched_data = {}
#         for tool in TOOLS:
#             result = call_mcp_tool(tool, session_id, base_url)
#             if result:
#                 st.session_state.fetched_data[tool] = result


############################## NEWS ANALYSIS ###################################################################
# def extract_portfolio_keywords() -> list[str]:
#     data = st.session_state.get("fetched_data", {})
#     keywords = set()

#     mf = data.get("fetch_mf_transactions", [])
#     stocks = data.get("fetch_stock_transactions", [])

#     for txn in mf:
#         if name := txn.get("fund_name") or txn.get("scheme"):
#             keywords.add(name.split()[0])  # Add only first word or parse fully

#     for stk in stocks:
#         if symbol := stk.get("stock_name") or stk.get("symbol"):
#             keywords.add(symbol.split()[0])

#     return list(keywords)


#################################################################

