""" Credit Report Agent for Credit Analysis"""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt


credit_report_agent = Agent(
    model="gemini-2.0-flash",
    name="credit_report_agent",
    instruction=prompt.credit_report_agent_prompt,
    output_key="credit_report_output",
    tools=[google_search],  # Ensure google_search is properly imported and configured
)




# from google.adk import Agent
# from google.adk.tools import google_search, FunctionTool
# from utils.load_json import load_json_from_session  # centralized import
# from . import prompt
# import json

# def summarize_credit_report_tool(ctx):
#     session_id = ctx.get("session_id", "default")
#     credit_data = load_json_from_session(session_id, "fetch_credit_report")

#     if not credit_data:
#         return "⚠️ Credit report data missing for session."

#     return f"Summarize this structured credit report data:\n{json.dumps(credit_data, indent=2)}"

# credit_report_agent = Agent(
#     model="gemini-2.0-flash",
#     name="credit_report_agent",
#     description="Summarizes user's credit report from JSON with analysis and recommendations.",
#     instruction=prompt.credit_report_agent_prompt,
#     output_key="credit_report_output",
#     tools=[
#         google_search,
#         FunctionTool(func=summarize_credit_report_tool)
#     ]
# )
