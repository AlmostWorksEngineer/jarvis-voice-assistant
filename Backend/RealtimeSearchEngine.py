import datetime
import os
from json import load, dump
from googlesearch import search
from groq import Groq
from dotenv import load_dotenv

# --- DYNAMIC PATH SETUP ---
# Gets the 'Backend' folder path
current_dir = os.path.dirname(os.path.abspath(__file__))
# Moves up to the 'JARVIS AI' folder path
base_dir = os.path.dirname(current_dir)
# Path for .env and ChatLog
env_path = os.path.join(base_dir, ".env")
chat_log_path = os.path.join(base_dir, "Data", "ChatLog.json")

# Load environment variables
load_dotenv(env_path)

Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")
GroqAPIKey = os.getenv("GroqAPIKey")

# Initialize the Groq client
client = Groq(api_key=GroqAPIKey)

# Define the system instructions
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Ensure Data directory exists and load ChatLog
os.makedirs(os.path.dirname(chat_log_path), exist_ok=True)
try:
    with open(chat_log_path, "r") as f:
        messages = load(f)
except Exception:
    with open(chat_log_path, "w") as f:
        dump([], f)
    messages = []

def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    return Answer

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

def Information():
    now = datetime.datetime.now()
    return (f"Use This Real-time Information if needed:\n"
            f"Day: {now.strftime('%A')}\nDate: {now.strftime('%d')}\n"
            f"Month: {now.strftime('%B')}\nYear: {now.strftime('%Y')}\n"
            f"Time: {now.strftime('%H:%M:%S')}\n")

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages
    
    with open(chat_log_path, "r") as f:
        messages = load(f)
        
    messages.append({"role": "user", "content": f"{prompt}"})
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})
    
    # UPDATED MODEL NAME HERE: llama-3.3-70b-versatile
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True
    )
    
    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
            
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    
    with open(chat_log_path, "w") as f:
        dump(messages, f, indent=4)
        
    SystemChatBot.pop()
    return AnswerModifier(Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))