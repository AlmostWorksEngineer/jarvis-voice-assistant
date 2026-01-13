import os
from groq import Groq
from rich import print
from dotenv import load_dotenv

# --- DYNAMIC PATH SETUP ---
# Ensures the script looks in the JARVIS AI folder for .env
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)
env_path = os.path.join(base_dir, ".env")

# Load environment variables
load_dotenv(env_path)

# Retrieve Groq API key (Make sure GROQ_API_KEY is in your .env)
GroqAPIKey = os.getenv("GroqAPIKey")

# Initialize the Groq client
client = Groq(api_key=GroqAPIKey)

# Recognized function keywords for task categorization
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

# System preamble for the Decision-Making Model
preamble = """
You are a very accurate Decision-Making Model. 
Your task is to categorize the user's query into specific commands.
*** Do not answer the query. Only respond with the command structure. ***

-> Respond with 'general ( query )' for basic conversation.
-> Respond with 'realtime ( query )' for news or current info.
-> Respond with 'open (application)' for opening apps.
-> Respond with 'exit' to end the session.
"""

# Example interactions for context (Shot prompting)
ChatHistory = [
    {"role": "user", "content": "how are you?"},
    {"role": "assistant", "content": "general how are you?"},
    {"role": "user", "content": "open chrome and tell me about mahatma gandhi."},
    {"role": "assistant", "content": "open chrome, general tell me about mahatma gandhi."}
]

def FirstLayerDMM(prompt: str = "test"):
    try:
        # Using llama-3.3-70b-versatile for high-speed decision making
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": preamble}
            ] + ChatHistory + [
                {"role": "user", "content": prompt}
            ],
            temperature=0.1, # Keep temperature low for precise command output
            max_tokens=100
        )

        response = completion.choices[0].message.content.strip()
        
        # Process and filter valid tasks
        tasks = [t.strip() for t in response.replace("\n", "").split(",")]
        valid_tasks = []
        for task in tasks:
            for func in funcs:
                if task.lower().startswith(func):
                    valid_tasks.append(task)
                    break
        
        return valid_tasks

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        if user_input.strip():
            print(FirstLayerDMM(user_input))