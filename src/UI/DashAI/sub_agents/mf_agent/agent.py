""" Mutual Fund Agent for Mutual Fund Analysis"""
from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL="gemini-2.0-flash"

mf_agent = Agent(
    model=MODEL,
    name="mf_agent",
    instruction=prompt.mf_agent_prompt,
    output_key="mf_agent_output",
    tools=[google_search],  # Ensure google_search is properly imported and configured
)

# """Mutual Fund Agent for Mutual Fund Analysis"""

# from google.adk import Agent
# from google.adk.tools import google_search, FunctionTool
# from utils.load_json import load_json_from_session
# from . import prompt
# import json

# MODEL = "gemini-2.5-pro"

# def summarize_mf_portfolio(ctx):
#     session_id = ctx.get("session_id", "default")
#     mf_data = load_json_from_session(session_id, "fetch_mf_transactions")

#     if not mf_data:
#         return "⚠️ No mutual fund transaction data found for this session. Please upload or fetch it first."

#     return f"Analyze and summarize this mutual fund portfolio data:\n{json.dumps(mf_data, indent=2)}"

# mf_agent = Agent(
#     model=MODEL,
#     name="mf_agent",
#     description="Analyzes mutual fund transaction data to summarize portfolio performance, allocation, and suggestions.",
#     instruction=prompt.mf_agent_prompt,
#     output_key="mf_agent_output",
#     tools=[
#         google_search,
#         FunctionTool(func=summarize_mf_portfolio)
#     ]
# )
