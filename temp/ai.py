import os
from dotenv import load_dotenv

# Use find_dotenv or specify path to ensure the .env in the root is found
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

# Configuration
endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"
token = os.environ.get("GITHUB_TOKEN")

if not token:
    print("WARNING: GITHUB_TOKEN environment variable not set. Please check your .env file.")
    # Fallback to direct token if needed for debugging or prompt user
    # token = input("Please enter your GitHub Token: ").strip()

# Create client
client = None
if token:
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
        model=model
    )

# Conversation history
conversation_history = [
    SystemMessage(content="You are a helpful assistant.")
]

def get_ai_response(user_input):
    """Get response from AI"""
    if not client:
        return "Error: Client not initialized. Check GITHUB_TOKEN."
    
    conversation_history.append(UserMessage(content=user_input))
    
    try:
        # Get AI response
        response = client.complete(
            messages=conversation_history,
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model
        )
        
        # Extract response
        ai_response = response.choices[0].message.content
        conversation_history.append(AssistantMessage(content=ai_response))
        return ai_response
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print(f"Chatbot started (Model: {model}). Type 'quit' or 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        response = get_ai_response(user_input)
        print(f"AI: {response}")