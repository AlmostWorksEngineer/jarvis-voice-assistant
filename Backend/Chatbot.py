from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# ================= LOAD ENV =================

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

# ================= CHAT MEMORY =================

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": System}
]

# Load chat log
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# ================= REALTIME INFO =================

def RealtimeInformation():
    now = datetime.datetime.now()

    day = now.strftime("%A")
    date = now.strftime("%d")
    month = now.strftime("%B")
    year = now.strftime("%Y")
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    second = now.strftime("%S")

    data = (
        "Use this real-time information if needed:\n"
        f"Day: {day}\n"
        f"Date: {date}\n"
        f"Month: {month}\n"
        f"Year: {year}\n"
        f"Time: {hour}:{minute}:{second}\n"
    )

    return data

# ================= ANSWER CLEANER =================

def AnswerModifier(answer):
    lines = answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

# ================= CHATBOT =================

def ChatBot(Query):
    global messages

    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
    except:
        messages = []

    messages.append({"role": "user", "content": Query})

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=(
            SystemChatBot
            + [{"role": "system", "content": RealtimeInformation()}]
            + messages
        ),
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True
    )

    Answer = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.replace("</s>", "")
    Answer = AnswerModifier(Answer)

    messages.append({"role": "assistant", "content": Answer})

    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    return Answer

# ================= TEST =================

if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        print(ChatBot(user_input))
