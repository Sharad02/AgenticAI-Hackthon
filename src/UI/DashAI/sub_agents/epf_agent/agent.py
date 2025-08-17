""" EPF Agent for EPF Analysis"""
from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL="gemini-2.0-flash"

epf_agent = Agent(
    model=MODEL,
    name="epf_agent",
    instruction=prompt.epf_agent_prompt,
    output_key="epf_agent_output",
    tools=[google_search],  # Ensure google_search is properly imported and configured
)


# """EPF Agent for EPF Analysis"""

# from google.adk import Agent
# from google.adk.tools import google_search, FunctionTool
# from utils.load_json import load_json_from_session
# from . import prompt
# import json

# MODEL = "gemini-2.5-pro"

# def summarize_epf_data(ctx):
#     session_id = ctx.get("session_id", "default")
#     epf_data = load_json_from_session(session_id, "fetch_epf_details")

#     if not epf_data:
#         return "⚠️ EPF data is missing or unavailable. Please check if 'fetch_epf_details.json' is loaded."

#     return f"Analyze the following EPF data:\n{json.dumps(epf_data, indent=2)}"

# epf_agent = Agent(
#     model=MODEL,
#     name="epf_agent",
#     description="Summarizes EPF account and contribution details using structured data, and provides user-friendly insights and suggestions.",
#     instruction=prompt.epf_agent_prompt,
#     output_key="epf_agent_output",
#     tools=[
#         google_search,
#         FunctionTool(func=summarize_epf_data)
#     ]
# )
