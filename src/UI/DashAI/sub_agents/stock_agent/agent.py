""" Stock Agent for Stock Analysis"""

from google.adk import Agent
from google.adk.tools import google_search


from . import prompt

MODEL="gemini-2.0-flash"

stock_agent = Agent(
    model=MODEL,
    name="stock_agent",
    instruction=prompt.stock_agent_prompt,
    output_key="stock_agent_output",
    tools=[google_search],  # Ensure google_search is properly imported and configured

    )


# """Stock Agent for Stock Analysis"""

# from google.adk import Agent
# from google.adk.tools import google_search, FunctionTool
# from utils.load_json import load_json_from_session
# from . import prompt
# import json

# MODEL = "gemini-2.5-pro"

# def summarize_stock_data(ctx):
#     session_id = ctx.get("session_id", "default")
#     stock_data = load_json_from_session(session_id, "fetch_stock_transactions")

#     if not stock_data:
#         return "⚠️ Stock transaction data not found. Please ensure 'fetch_stock_transactions.json' is available."

#     return f"Here is the stock transaction data to analyze:\n{json.dumps(stock_data, indent=2)}"

# stock_agent = Agent(
#     model=MODEL,
#     name="stock_agent",
#     description="Analyzes stock transaction history to summarize holdings, trading patterns, and unrealized performance.",
#     instruction=prompt.stock_agent_prompt,
#     output_key="stock_agent_output",
#     tools=[
#         google_search,
#         FunctionTool(func=summarize_stock_data)
#     ]
# )
