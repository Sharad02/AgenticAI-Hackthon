# DashAI/sip.py
import math

# Optional: If you want to explicitly state that a parameter can be None
# from typing import Optional
from typing import Optional

def financial_calculator_and_analyzer(
    type: str,
    monthly_investment: Optional[int] = None,
    annual_return_percent: Optional[int] = None,
    years: Optional[int] = None,
    fund_name: Optional[str] = None,
    current_nav: Optional[int] = None,
    five_year_cagr: Optional[int] = None,
    ten_year_cagr: Optional[int] = None,
    lump_sum_investment: Optional[int] = None
) -> str:
    
    """
    Performs SIP maturity calculation or analyzes mutual fund growth and projections using dynamically provided data.

    "A versatile financial tool that performs SIP maturity calculations or analyzes mutual fund growth and projections. "
        "For SIP, it requires 'monthly_investment', 'annual_return_percent', and 'years'. "
        "For Mutual Fund analysis, it requires 'fund_name', 'current_nav', 'five_year_cagr', and 'ten_year_cagr' "
        "(these growth rates and NAV should be obtained by performing a Google Search first). "
        "It can then project future value if 'years' and either 'monthly_investment' or 'lump_sum_investment' are also provided."

    Args:
        type (str): Specifies the calculation type: "SIP" or "Mutual Fund".
        monthly_investment (float, optional): Monthly SIP installment amount. Required for "SIP" type and for MF projection (if not lump sum).
        annual_return_percent (float, optional): Expected annual rate of return in percentage (e.g., 12 for 12%). Required for "SIP" type.
        years (int, optional): The investment duration in years. Required for both "SIP" and "Mutual Fund" projection.
        fund_name (str, optional): The name of the mutual fund to analyze. Required for "Mutual Fund" type.
        current_nav (float, optional): The current Net Asset Value (NAV) of the mutual fund. Required for "Mutual Fund" type analysis.
        five_year_cagr (float, optional): The 5-year Compound Annual Growth Rate (CAGR) in percentage. Required for "Mutual Fund" type analysis.
        ten_year_cagr (float, optional): The 10-year Compound Annual Growth Rate (CAGR) in percentage. Required for "Mutual Fund" type analysis.
        lump_sum_investment (float, optional): One-time investment amount for mutual fund projection. Used for "Mutual Fund" type if monthly_investment is not provided.

    Returns:
        str: A formatted string with the calculation results or analysis.
    """

    if type == "SIP":
        if monthly_investment is None or annual_return_percent is None or years is None:
            return "Please provide monthly investment, annual return percentage, and years for SIP calculation."
        if monthly_investment <= 0 or annual_return_percent < 0 or years <= 0:
            return "Please provide valid positive values for monthly investment, annual return, and years."

        monthly_rate = (annual_return_percent / 100) / 12
        num_months = years * 12

        if monthly_rate == 0:
            maturity_amount = monthly_investment * num_months
        else:
            maturity_amount = monthly_investment * ((pow(1 + monthly_rate, num_months) - 1) / monthly_rate) * (1 + monthly_rate)

        total_invested_amount = monthly_investment * num_months

        return (
            f"SIP Maturity Calculation:\n"
            f"Monthly Investment: ₹{monthly_investment:,.2f}\n"
            f"Annual Return: {annual_return_percent}%\n"
            f"Duration: {years} years\n"
            f"Total Invested Amount: ₹{total_invested_amount:,.2f}\n"
            f"Estimated Maturity Amount: ₹{maturity_amount:,.2f}"
        )

    elif type == "Mutual Fund":
        if not fund_name:
            return "Please provide the name of the mutual fund to analyze."

        # Ensure dynamic data is provided by the LLM (from search results)
        if current_nav is None or five_year_cagr is None or ten_year_cagr is None:
            return (f"Missing current NAV, 5-year CAGR, or 10-year CAGR for {fund_name}. "
                    "I need these values, please provide them or ensure the coordinator searched for them.")

        response = f"Analysis for {fund_name} (data dynamically retrieved):\n"
        response += f"Current NAV: ₹{current_nav:.2f}\n"
        response += f"Last 5 years growth rate (CAGR): {five_year_cagr}%\n"
        response += f"Last 10 years growth rate (CAGR): {ten_year_cagr}%\n"

        # Project future investment
        if years is not None and (monthly_investment is not None or lump_sum_investment is not None):
            # Use 5-year CAGR as default projection rate, or 10-year if 5-year is not available/relevant
            expected_annual_rate_for_projection = five_year_cagr

            response += f"\nProjected growth for {years} years (assuming {expected_annual_rate_for_projection}% annual return based on 5-year CAGR):\n"

            if lump_sum_investment is not None:
                if lump_sum_investment <= 0:
                    return "Lump sum investment must be positive."
                future_value = lump_sum_investment * pow(1 + (expected_annual_rate_for_projection / 100), years)
                response += f"If you invest a lump sum of ₹{lump_sum_investment:,.2f}:\n"
                response += f"Estimated value after {years} years: ₹{future_value:,.2f}\n"
            elif monthly_investment is not None:
                if monthly_investment <= 0:
                    return "Monthly investment must be positive."
                monthly_rate = (expected_annual_rate_for_projection / 100) / 12
                num_months = years * 12
                if monthly_rate == 0: # Handle 0% return case
                    future_value = monthly_investment * num_months
                else:
                    future_value = monthly_investment * ((pow(1 + monthly_rate, num_months) - 1) / monthly_rate) * (1 + monthly_rate)
                total_invested_amount = monthly_investment * num_months
                response += f"If you invest ₹{monthly_investment:,.2f} per month:\n"
                response += f"Total Invested Amount: ₹{total_invested_amount:,.2f}\n"
                response += f"Estimated value after {years} years: ₹{future_value:,.2f}\n"
        else:
            response += "\nTo get a projection, please specify an investment amount (monthly or lump sum) and number of years."

        return response

    else:
        return "Invalid 'type' specified. Please choose 'SIP' or 'Mutual Fund'."
