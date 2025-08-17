import os
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

# Hardcoded path to the local service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  "/app/agentic-ai-466415-5a1005031578.json" #gcp path
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/workspaces/AgenticAI-Hackthon/src/UI/agentic-ai-466415-5a1005031578.json"
# print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
# Initialize Vertex AI
aiplatform.init(project="agentic-ai-466415", location="us-central1")

# Load Gemini model
model = GenerativeModel("gemini-2.0-flash")

# Generate response
def get_vertex_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini Error: {e}"

# vertex_chat.py

