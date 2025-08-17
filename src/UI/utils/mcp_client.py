# utils/mcp_client.py
import requests
import json

BASE_URL = "https://fi-mcp-mock-292450254722.us-central1.run.app"

def fetch_tool_result(tool_name: str, session_id: str):
    tool_url = f"{BASE_URL}/mcp/stream"
    params = {"toolName": tool_name, "sessionId": session_id}
    resp = requests.get(tool_url, params=params)

    if "application/json" in resp.headers.get("Content-Type", ""):
        return resp.json()
    elif "text" in resp.headers.get("Content-Type", ""):
        try:
            return json.loads(resp.text)
        except:
            return None
    return None
