import os
from dotenv import load_dotenv
load_dotenv()

import json
import asyncio
from google.cloud import aiplatform
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import FunctionTool
# Use FirestoreSessionService in production for persistence across sessions
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Assuming these are in a 'prompt' directory or module
from DashAI import prompt # Ensure 'prompt.py' exists and contains DashAI_financial_coordinator_prompt

# Assuming these are in a 'tools' directory
from DashAI.tools.sip_calculator_tool import financial_calculator_and_analyzer
from DashAI.tools.read_json_file import get_all_financial_data

# --- Sub-Agent Imports ---
from DashAI.sub_agents.credit_report_agent import credit_report_agent
from DashAI.sub_agents.data_bank_transaction_agent import data_bank_transaction_agent
from DashAI.sub_agents.epf_agent import epf_agent
from DashAI.sub_agents.mf_agent import mf_agent
from DashAI.sub_agents.net_worth_agent import net_worth_agent
from DashAI.sub_agents.stock_agent import stock_agent


import uuid
import requests # This import seems unused if not handling external APIs directly.

# --- Environment Variable Setup ---
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/workspaces/AgenticAI-Hackthon/src/UI/agentic-ai-466415-5a1005031578.json"

# --- AI Platform Initialization ---
aiplatform.init(
    project="agentic-ai-466415",
    location="us-central1"
)

# --- Session Management Configuration ---
app_name = "viz_app"
user_id = "jeny" # In a real app, this would be dynamically generated or passed from auth
# current_session_id = None # This global is no longer needed

# --- DashAI Financial Orchestrator Agent ---
DashAI_financial_coordinator = LlmAgent(
    name="DashAI_financial_coordinator",
    model="gemini-2.0-flash", # Consider "gemini-1.5-flash-001" or "gemini-1.5-pro-001" for newer models
    description=(
        "DashAI is a financial conversation orchestrator that intelligently routes user queries to specialized agents, "
        "manages session state, and delegates tool invocation across credit, EPF, investments, banking, and net worth domains."
    ),
    instruction= prompt.DashAI_financial_coordinator_prompt, # Ensure prompt.py has this variable
    output_key="DashAI_financial_coordinator_output",
    tools=[
        AgentTool(agent=credit_report_agent),
        AgentTool(agent=data_bank_transaction_agent),
        AgentTool(agent=epf_agent),
        AgentTool(agent=mf_agent),
        AgentTool(agent=net_worth_agent),
        AgentTool(agent=stock_agent),
        FunctionTool(func=financial_calculator_and_analyzer),
        FunctionTool(func=get_all_financial_data)
    ],
)

root_agent = DashAI_financial_coordinator

# --- Session and Runner Setup ---
# This function is now modified to handle session_id more dynamically
async def setup_session_and_runner(current_user_id: str, current_session_id: str):
    # Use FirestoreSessionService in production for persistence across sessions
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=app_name,
        user_id=current_user_id,
        session_id=current_session_id
    )
    runner = Runner(agent=root_agent, app_name=app_name, session_service=session_service)
    return session, runner

# Modified call_agent_async to accept session_id
async def call_agent_async(query: str, session_id: str, user_id: str = "default_user"):
    """
    Calls the root ADK agent and processes the events to return the final response.
    It takes the session_id from Streamlit's st.session_state to maintain conversation history.
    """
    # Use the provided session_id instead of generating a new one
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner(user_id, session_id) # Pass user_id and session_id

    final_response_text = "No response from agent." # Default message

    try:
        # Pass the correct user_id and session_id to run_async
        events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)

        async for event in events:
            # print(f"Event received: {event}") # For debugging agent events
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                break # Exit the loop once the final response is found
            # You might want to capture intermediate thoughts or tool calls for debugging/display
            # else:
            #     # Optional: print or log intermediate events
            #     if event.content and event.content.parts:
            #         print(f"Intermediate: {event.content.parts[0].text}")

    except Exception as e:
        print(f"Error during agent execution: {e}")
        final_response_text = f"An error occurred with the agent: {e}"

    print(f"DashAI: {final_response_text}") # Print the agent's response to the console
    return final_response_text

# The __main__ block is for local testing of agentt.py only.
# When integrated with Streamlit, Streamlit will manage the event loop.
async def run_local_test():
    print("\nWelcome to DashAI – Your Conversational Financial Assistant (Local Test)\n")
    print("Type your financial question (or type 'exit' to quit):")

    # For local testing, generate a single session ID for the entire session
    local_test_session_id = str(uuid.uuid4())
    local_test_user_id = "test_user_local"

    while True:
        query = input("\nYou: ")
        if query.strip().lower() in ["exit", "quit"]:
            print("\n👋 Goodbye! Thank you for using DashAI.")
            break

        # Pass the local test session ID and user ID
        await call_agent_async(query, local_test_session_id, local_test_user_id)

if __name__ == "__main__":
    asyncio.run(run_local_test()) # Run the async local test function once