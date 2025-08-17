#############################################################
import json
import streamlit as st
import pandas as pd
from modules.mcp_tools import call_mcp_tool, extract_and_clean_json

# --- Function to Fetch Cleaned Credit Report ---
def fetch_cleaned_credit_report(session_id: str, base_url: str) -> dict | None:
    tool = "fetch_credit_report"
    result = call_mcp_tool(tool, session_id, base_url)
    if result:
        return extract_and_clean_json(result)
    return None


# --- Session ID and Base URL ---
session_id = st.session_state.get("session_id")
base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

# --- Fetch Data ---
cleaned_data = fetch_cleaned_credit_report(session_id, base_url)

if cleaned_data:
    kpis = extract_and_clean_json(cleaned_data)
    # st.subheader("📄 Cleaned Credit Report (JSON)")
    # st.json(cleaned_data)

    # Extracting simple fields for table view
    report = cleaned_data.get("creditReports", [{}])[0].get("creditReportData", {})
    # report = cleaned_data.get("creditReport", {})

    if report:
        # Convert to DataFrame for table view
        report_df = pd.DataFrame.from_dict(report, orient='index', columns=['Value']).reset_index()
        report_df.columns = ['Field', 'Value']
        # st.subheader("📊 Credit Report Summary (Table)")
        # st.table(report_df)
    else:
        st.warning("No 'creditReport' section found in response.")
else:
    cleaned_data=0


def extract_credit_kpis(credit_data: dict) -> dict:
    try:
        report_data = credit_data["creditReports"][0]["creditReportData"]

        # 1. Credit Score
        credit_score = int(report_data.get("score", {}).get("bureauScore", 0))
        if credit_score >= 750:
            credit_score_benchmark = "Excellent 🔺"
        elif 650 <= credit_score < 750:
            credit_score_benchmark = "Average ➡️"
        else:
            credit_score_benchmark = "Poor 🔻"

        # 2. Total Outstanding Balance
        total_outstanding = int(
            report_data.get("creditAccount", {})
                        .get("creditAccountSummary", {})
                        .get("totalOutstandingBalance", {})
                        .get("outstandingBalanceAll", 0)
        )

        # 3–5. Loop through account details
        account_details = report_data.get("creditAccount", {}).get("creditAccountDetails", [])
        total_past_due = 0
        total_current_balance = 0
        total_credit_limit = 0
        missed_payment_accounts = 0

        for acc in account_details:
            try:
                total_past_due += int(acc.get("amountPastDue", 0))
                total_current_balance += int(acc.get("currentBalance", 0))
                total_credit_limit += int(acc.get("highestCreditOrOriginalLoanAmount", 0))

                if int(acc.get("paymentRating", 0)) > 0:
                    missed_payment_accounts += 1
            except Exception:
                continue

        # 4. Average Credit Utilization
        avg_utilization = (
            (total_current_balance / total_credit_limit) * 100
            if total_credit_limit else 0
        )

        # 5. Missed Payment Benchmarking
        missed_change = "⚠️ High risk" if missed_payment_accounts > 0 else "✅ Acceptable"

        return {
            "CREDIT_SCORE": {
                "value": credit_score,
                "benchmark": credit_score_benchmark,  # <- benchmark key instead of change
                "unit": "",
                "icon": "💳"
            },
            "TOTAL_OUTSTANDING_BALANCE": {
                "value": total_outstanding,
                "change": "",
                "unit": "₹",
                "icon": "📂"
            },
            "TOTAL_PAST_DUE_AMOUNT": {
                "value": total_past_due,
                "change": "",
                "unit": "₹",
                "icon": "⚠️"
            },
            "AVERAGE_CREDIT_UTILIZATION": {
                "value": f"{round(avg_utilization, 2)}",
                "change": "",
                "unit": "%",
                "icon": "📊"
            },
            "ACCOUNTS_WITH_MISSED_PAYMENTS": {
                "value": missed_payment_accounts,
                "change": missed_change,
                "unit": "",
                "icon": "❗"
            }
        }

    except Exception as e:
        return {"ERROR": {"value": str(e), "change": ""}}

#######################
# # modules/kpi_definitions/credit.py
# # Contains KPI calculations related to credit.

# def get_credit_score():
#     """
#     Placeholder function to get the user's credit score.
#     In a real app, this would read credit_report.json.

#     Returns a hardcoded value for the prototype.
#     """
#     # In the future, you could use json here:
#     # import json
#     # with open('data/USER_ALEX/credit_report.json', 'r') as f:
#     #     data = json.load(f)
#     # score = data['credit_score']
#     # change = score - data['previous_score']
#     return {'value': 780, 'change': 10}
