############# NIRPU ########################
import streamlit as st
import os
import json
from typing import Dict
from modules.mcp_tools import call_mcp_tool, extract_and_clean_json
import pandas as pd
from datetime import datetime
from collections import defaultdict

# --- Session and Base URL ---
# These are typically handled by the calling script (e.g., 1_Dashboard.py)
# and passed to functions. Keeping them here for completeness if this file
# were to be run standalone for testing, but they are usually not global in a module.
session_id = st.session_state.get("session_id")
base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

# --- Function to Fetch Cleaned Data for fetch_bank_transactions ---
def fetch_cleaned_bank_transactions(session_id: str, base_url: str) -> dict | None:
    tool = "fetch_bank_transactions"
    result = call_mcp_tool(tool, session_id, base_url)
    if result:
        return extract_and_clean_json(result)
    return None

# --- Function to Extract KPIs from Cleaned Bank Data ---
def extract_selected_banking_kpis(cleaned_data: dict) -> dict:
    total_credit = 0.0
    total_debit = 0.0
    transaction_count = 0
    total_transaction_amount = 0.0
    upi_count = 0
    upi_transaction_amount = 0.0

    # Group net flow by (YYYY-MM)
    monthly_cash_flow = defaultdict(lambda: {'credit': 0.0, 'debit': 0.0})

    for account in cleaned_data.get("bankTransactions", []):
        for txn in account.get("txns", []):
            try:
                amount = float(txn[0])
                narration = txn[1]
                txn_date = datetime.strptime(txn[2], "%Y-%m-%d")
                txn_type = int(txn[3])
                mode = txn[4].upper() if isinstance(txn[4], str) else ""

                key = txn_date.strftime("%Y-%m")

                if txn_type == 1:
                    total_credit += amount
                    monthly_cash_flow[key]['credit'] += amount
                elif txn_type == 2:
                    total_debit += amount
                    monthly_cash_flow[key]['debit'] += amount

                if txn_type in [1, 2]:
                    transaction_count += 1
                    total_transaction_amount += abs(amount)

                if "UPI" in narration.upper():
                    upi_count += 1
                    upi_transaction_amount += abs(amount)

            except Exception:
                continue

    avg_transaction = total_transaction_amount / transaction_count if transaction_count else 0
    total_txns = sum(len(acc.get("txns", [])) for acc in cleaned_data.get("bankTransactions", []))
    upi_dominance = (upi_count / total_txns * 100) if total_txns else 0

    # Sort and calculate change in net cash flow
    sorted_months = sorted(monthly_cash_flow.keys())
    current_month = sorted_months[-1] if sorted_months else None
    prev_month = sorted_months[-2] if len(sorted_months) >= 2 else None

    net_cash_flow = round(total_credit - total_debit)
    net_cash_flow_prev = 0

    if prev_month:
        net_cash_flow_prev = monthly_cash_flow[prev_month]['credit'] - monthly_cash_flow[prev_month]['debit']

    net_cash_change = net_cash_flow - net_cash_flow_prev
    change_str = f"{'▲' if net_cash_change >= 0 else '▼'} {abs(net_cash_change):,.0f} from {prev_month}" if prev_month else ""

    return {
        "Net Cash Flow": net_cash_flow,
        "Net Cash Flow Change": change_str,
        "Total Credit Amount": round(total_credit),
        "Total Debit Amount": round(total_debit),
        "Average Transaction Amount": round(avg_transaction, 2),
        "Total Transactions": total_txns,
        "UPI Transaction Count": upi_count,
        "UPI Transaction Amount": round(upi_transaction_amount, 2),
        "UPI Transaction Dominance (%)": round(upi_dominance, 2)
    }

# --- Function to Get Selected Banking KPIs for UI Display ---
def get_selected_banking_kpis(cleaned_data: dict) -> dict:
    # Call the internal KPI extraction function
    kpis = extract_selected_banking_kpis(cleaned_data)

    # Prepare NET_CASH_FLOW KPI with conditional benchmark
    net_cash_flow_kpi = {
        "value": kpis["Net Cash Flow"],
        "change": kpis.get("Net Cash Flow Change", ""),
        "unit": "₹",
        "icon": "💸",
        "benchmark": "" # Initialize benchmark
    }

    # If 'Net Cash Flow Change' is not present (empty string), set a benchmark based on current value
    if not net_cash_flow_kpi["change"]:
        net_cash_value = kpis["Net Cash Flow"]
        formatted_net_cash_value = f"₹{net_cash_value:,.0f}" # Format the value

        if net_cash_value > 0:
            net_cash_flow_kpi["benchmark"] = f"{formatted_net_cash_value} Positive ⬆️"
        elif net_cash_value < 0:
            # If value is negative, show the formatted value and "Negative" with down arrow
            net_cash_flow_kpi["benchmark"] = f"{formatted_net_cash_value} Negative ⬇️"
        else:
            net_cash_flow_kpi["benchmark"] = f"{formatted_net_cash_value} Neutral ↔️"

    return {
        "NET_CASH_FLOW": net_cash_flow_kpi,
        "TOTAL_CREDIT": {
            "value": kpis["Total Credit Amount"],
            "change": "",
            "unit": "₹",
            "icon": "🟢"
        },
        "TOTAL_DEBIT": {
            "value": kpis["Total Debit Amount"],
            "change": "",
            "unit": "₹",
            "icon": "🔴"
        },
        "UPI_DOMINANCE": {
            "value": f'{kpis["UPI Transaction Dominance (%)"]}',
            "change": "",
            "unit": "%",
            "icon": "📱"
        }
    }



# banking.py
banking_kpis = {
    'NET_CASH_FLOW': {'value': 0, 'change': '', 'unit': '₹', 'icon': '💸', 'title': "Net Cash Flow"},
    'TOTAL_CREDIT': {'value': 0, 'change': '', 'unit': '₹', 'icon': '🟢', 'title': "Total Credit"},
    'TOTAL_DEBIT': {'value': 0, 'change': '', 'unit': '₹', 'icon': '🔴', 'title': "Total Debit"},
    'UPI_DOMINANCE': {'value': '0%', 'change': '', 'unit': '', 'icon': '📱', 'title': "UPI Dominance", 'benchmark_key': 'change'}
}

def get_banking_kpi(kpi_name):
    return banking_kpis.get(kpi_name, {'value': 0, 'change': '', 'unit': '', 'icon': ''})








######################################################## OLD ####################################
# # modules/kpi_definitions/banking.py
# # Contains KPI calculations related to banking and cash flow.

# def calculate_savings_rate():
#     """
#     Placeholder function to calculate the user's savings rate.
#     In a real app, this would read bank_transactions.csv and perform
#     (Income - Spending) / Income.

#     Returns a hardcoded value for the prototype.
#     """
#     # In the future, you could use pandas here:
#     # import pandas as pd
#     # df = pd.read_csv('data/USER_ALEX/bank_transactions.csv')
#     # income = df[df['category'] == 'Income']['amount'].sum()
#     # spending = df[(df['amount'] < 0) & (df['category'] != 'Transfers')]['amount'].sum()
#     # savings_rate = ((income + spending) / income) * 100
#     return {'value': 22, 'change': -1.5}
