import os
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

# This script demonstrates how to use the Vertex AI SDK to generate text 
# with a specific prompt using a Gemini model.

# --- Configuration ---
# Set the path to your Google Cloud service account key file.
# IMPORTANT: Replace this path with the actual path to your credentials file.
# Example for a local environment:
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-file.json"
# Example for a specific workspace setup:
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/workspaces/AgenticAI-Hackthon/src/UI/agentic-ai-466415-5a1005031578.json"

# --- Vertex AI Initialization ---
# Initialize the Vertex AI SDK with your project and location.
# Replace "agentic-ai-466415" with your Google Cloud project ID.
try:
    aiplatform.init(project="agentic-ai-466415", location="us-central1")
    print("Vertex AI initialized successfully.")
except Exception as e:
    print(f"Error initializing Vertex AI: {e}")
    # Exit if initialization fails, as the rest of the script cannot run.
    exit()

# --- Model Loading ---
# Load the specified Generative Model from Vertex AI.
# Here, we are using "gemini-2.0-flash".
try:
    model = GenerativeModel("gemini-2.0-flash")
    print("Gemini model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# --- Function to Generate Response ---
def get_vertex_response(prompt: str) -> str:
    """
    Sends a prompt to the Gemini model and returns the generated text response.

    Args:
        prompt: The text prompt to send to the model.

    Returns:
        The model's generated text response, or an error message if something goes wrong.
    """
    try:
        print(f"\nSending prompt to Gemini: '{prompt}'")
        response = model.generate_content(prompt)
        # Assuming the response object has a 'text' attribute with the content.
        return response.text
    except Exception as e:
        # Provide a clear error message if the API call fails.
        return f"⚠️ An error occurred while calling the Gemini API: {e}"

# --- Main Execution ---
if __name__ == "__main__":
    # Define the prompt you want to send to the model.
    agentic_ai_prompt = "what is agentic ai"
    
    # Call the function to get the response from the model.
    response_text = get_vertex_response(agentic_ai_prompt)
    
    # Print the final response to the console.
    print("\n--- Gemini Model Response ---")
    print(response_text)
    print("---------------------------\n")
