""" Net Worth Agent for Net Worth Analysis"""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL="gemini-2.0-flash"

net_worth_agent = Agent(
    model=MODEL,
    name="net_worth_agent",
    instruction=prompt.net_worth_agent_prompt,
    output_key="=net_worth_agent_output",
    tools=[google_search],  # Ensure google_search is properly imported and configured
)


# """Net Worth Agent for Net Worth Analysis"""

# from google.adk import Agent
# from google.adk.tools import google_search, FunctionTool
# from utils.load_json import load_json_from_session
# from . import prompt
# import json

# MODEL = "gemini-2.5-pro"

# def summarize_net_worth(ctx):
#     session_id = ctx.get("session_id", "default")
#     data = load_json_from_session(session_id, "fetch_net_worth")

#     if not data:
#         return "⚠️ Net worth data is not available. Please ensure 'fetch_net_worth.json' is available for this session."

#     return f"Here is the structured net worth data to analyze:\n{json.dumps(data, indent=2)}"

# net_worth_agent = Agent(
#     model=MODEL,
#     name="net_worth_agent",
#     description="Analyzes net worth across assets and liabilities, summarizing performance and portfolio composition.",
#     instruction=prompt.net_worth_agent_prompt,
#     output_key="net_worth_agent_output",
#     tools=[
#         google_search,
#         FunctionTool(func=summarize_net_worth)
#     ]
# )
