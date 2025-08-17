import json
import streamlit as st
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

# --- Session Variables ---
session_id = st.session_state.get("session_id")
base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

# --- KPI Imports ---
from modules.kpi_definitions.banking import get_selected_banking_kpis, fetch_cleaned_bank_transactions
from modules.kpi_definitions.credit import extract_credit_kpis, fetch_cleaned_credit_report
from modules.kpi_definitions.epf import extract_epf_kpis, fetch_cleaned_epf_report
from modules.kpi_definitions.net_worth import extract_net_worth_kpis, fetch_cleaned_net_worth
from modules.kpi_definitions.stock import extract_stock_kpis, fetch_cleaned_stock_data

def summary_strategic_print() -> dict:
    """
    Fetches cleaned data, extracts KPIs, and returns the strategic summary.
    Handles cases where KPI extraction might fail or return empty results,
    replacing them with 0 to prevent errors.
    """

    # Initialize KPI variables to 0, so they default to 0 if extraction fails or is empty
    banking_kpis = 0
    credit_kpis = 0
    epf_kpis = 0
    networth_kpis = 0
    stock_kpis = 0

    # --- Fetch Cleaned Data and Extract KPIs with Error Handling ---

    try:
        cleaned_banking_data = fetch_cleaned_bank_transactions(session_id, base_url)
        extracted_banking_kpis = get_selected_banking_kpis(cleaned_banking_data)
        if extracted_banking_kpis is not None and extracted_banking_kpis: # Check if not None and not empty
            banking_kpis = extracted_banking_kpis
        else:
            banking_kpis = 0 # Explicitly set to 0 if None or empty
    except Exception as e:
        print(f"Error fetching or extracting banking KPIs: {e}")
        banking_kpis = 0 # Ensure it's 0 on error

    try:
        cleaned_credit_data = fetch_cleaned_credit_report(session_id, base_url)
        extracted_credit_kpis = extract_credit_kpis(cleaned_credit_data)
        if extracted_credit_kpis is not None and extracted_credit_kpis:
            credit_kpis = extracted_credit_kpis
        else:
            credit_kpis = 0
    except Exception as e:
        print(f"Error fetching or extracting credit KPIs: {e}")
        credit_kpis = 0

    try:
        cleaned_epf_data = fetch_cleaned_epf_report(session_id, base_url)
        extracted_epf_kpis = extract_epf_kpis(cleaned_epf_data)
        if extracted_epf_kpis is not None and extracted_epf_kpis:
            epf_kpis = extracted_epf_kpis
        else:
            epf_kpis = 0
    except Exception as e:
        print(f"Error fetching or extracting EPF KPIs: {e}")
        epf_kpis = 0

    try:
        cleaned_net_worth_data = fetch_cleaned_net_worth(session_id, base_url)
        extracted_networth_kpis = extract_net_worth_kpis(cleaned_net_worth_data)
        if extracted_networth_kpis is not None and extracted_networth_kpis:
            networth_kpis = extracted_networth_kpis
        else:
            networth_kpis = 0
    except Exception as e:
        print(f"Error fetching or extracting net worth KPIs: {e}")
        networth_kpis = 0

    try:
        cleaned_stock_data = fetch_cleaned_stock_data(session_id, base_url)
        extracted_stock_kpis = extract_stock_kpis(cleaned_stock_data)
        if extracted_stock_kpis is not None and extracted_stock_kpis:
            stock_kpis = extracted_stock_kpis
        else:
            stock_kpis = 0
    except Exception as e:
        print(f"Error fetching or extracting stock KPIs: {e}")
        stock_kpis = 0

    return {
        "banking": banking_kpis,
        "credit": credit_kpis,
        "epf": epf_kpis,
        "net_worth": networth_kpis,
        "stock": stock_kpis
    }


# --- Run Summary ---
strategic_data = summary_strategic_print()
print(json.dumps(strategic_data, indent=2))  # Optional: Console debug print