import json
import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil import parser
from modules.mcp_tools import call_mcp_tool, extract_and_clean_json

# --- Function to Fetch Cleaned EPF Report ---
def fetch_cleaned_epf_report(session_id: str, base_url: str) -> dict | None:
    tool = "fetch_epf_details"
    result = call_mcp_tool(tool, session_id, base_url)
    if result:
        return extract_and_clean_json(result)
    return None

# --- Session ID and Base URL ---
session_id = st.session_state.get("session_id")
base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

# --- Utility: Calculate Date Duration ---
def calculate_duration(start_date: str, end_date: str) -> int:
    try:
        start = parser.parse(start_date, dayfirst=True)
        end = parser.parse(end_date, dayfirst=True)
        return (end - start).days
    except:
        return 0



# --- Fetch Data ---
cleaned_data = fetch_cleaned_epf_report(session_id, base_url)


if cleaned_data:
    kpis = extract_and_clean_json(cleaned_data)
    # st.subheader("📄 Cleaned EPF Report (JSON)")
    # st.json(cleaned_data)

    # Extracting simple fields for table view
    report = cleaned_data.get("uanAccounts", [{}])[0].get("rawDetails", {})
    if report:
        # Convert to DataFrame for table view (optional)
        flat_dict = {}
        overall = report.get("overall_pf_balance", {})
        for k, v in overall.items():
            if isinstance(v, dict):
                for subk, subv in v.items():
                    flat_dict[f"{k}_{subk}"] = subv
            else:
                flat_dict[k] = v
        report_df = pd.DataFrame.from_dict(flat_dict, orient='index', columns=['Value']).reset_index()
        report_df.columns = ['Field', 'Value']
        # st.subheader("📊 EPF Report Summary (Table)")
        # st.table(report_df)
    else:
        st.warning("No 'epfReport' section found in response.")
else:
    cleaned_data=0

# --- Function to Extract EPF KPIs ---
def extract_epf_kpis(epf_data: dict) -> dict:
    try:
        uan_accounts = epf_data.get("uanAccounts", [])
        total_pension_balance = 0
        total_pf_balance = 0
        total_employment_days = 0
        total_employee_contribution = 0
        inactive_accounts = 0

        for account in uan_accounts:
            raw_details = account.get("rawDetails", {})
            overall_balance = raw_details.get("overall_pf_balance", {})

            pension_bal = overall_balance.get("pension_balance")
            total_pension_balance += int(pension_bal) if pension_bal and pension_bal.isdigit() else 0

            pf_bal = overall_balance.get("current_pf_balance")
            total_pf_balance += int(pf_bal) if pf_bal and pf_bal.isdigit() else 0

            for est in raw_details.get("est_details", []):
                doj = est.get("doj_epf")
                doe = est.get("doe_epf")
                if doj and doe:
                    total_employment_days += calculate_duration(doj, doe)

                emp_credit = est.get("pf_balance", {}).get("employee_share", {}).get("credit")
                if emp_credit and emp_credit.isdigit():
                    total_employee_contribution += int(emp_credit)

                if doe:
                    inactive_accounts += 1

        employment_years = round(total_employment_days / 365.25, 2)

        return {
            "TOTAL_PENSION_BALANCE": {
                "value": total_pension_balance,
                "change": "",
                "unit": "₹",
                "icon": "🏦"
            },
            "CURRENT_PF_BALANCE": {
                "value": total_pf_balance,
                "change": "",
                "unit": "₹",
                "icon": "💰"
            },
            "TOTAL_EMPLOYMENT_DURATION": {
                "value": f"{employment_years} years",
                "change": "",
                "unit": "",
                "icon": "📅"
            },
            "TOTAL_EPF_CONTRIBUTION_EMPLOYEE": {
                "value": total_employee_contribution,
                "change": "",
                "unit": "₹",
                "icon": "👤"
            },
            "INACTIVE_ACCOUNTS": {
                "value": inactive_accounts,
                "change": "",
                "unit": "",
                "icon": "⚠️"
            }
        }

    except Exception as e:
        return {"ERROR": {"value": str(e), "change": ""}}

