""" Bank Transaction Agent for Bank Transaction Analysis"""


from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL="gemini-2.0-flash"

data_bank_transaction_agent = Agent(
    model=MODEL,
    name="bank_transaction_agent",
    instruction=prompt.bank_transaction_agent_prompt,
    output_key="bank_transaction_agent_output",
    tools=[google_search],  # Ensure google_search is properly imported and configured
)


# """Bank Transaction Agent for Bank Transaction Analysis"""

# from google.adk import Agent
# from google.adk.tools import google_search, FunctionTool
# from utils.load_json import load_json_from_session
# from . import prompt
# import json

# MODEL = "gemini-2.5-pro"

# def summarize_bank_txns_tool(ctx):
#     session_id = ctx.get("session_id", "default")
#     bank_data = load_json_from_session(session_id, "fetch_bank_transactions")

#     if not bank_data:
#         return "⚠️ No bank transaction data found for this session. Please check file availability."

#     return f"Please analyze the following bank transaction data:\n{json.dumps(bank_data, indent=2)}"

# data_bank_transaction_agent = Agent(
#     model=MODEL,
#     name="bank_transaction_agent",
#     description="Analyzes two months of bank transactions and provides detailed summaries and recommendations.",
#     instruction=prompt.bank_transaction_agent_prompt,
#     output_key="bank_transaction_agent_output",
#     tools=[
#         google_search,
#         FunctionTool(func=summarize_bank_txns_tool)
#     ]
# )
