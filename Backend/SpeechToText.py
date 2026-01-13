import os
import mtranslate as mt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# --- DYNAMIC PATH SETUP ---
# Ensures the script looks in the root 'JARVIS AI' folder for .env and Data
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)
env_path = os.path.join(base_dir, ".env")

# Load environment variables
load_dotenv(env_path)
InputLanguage = os.getenv("InputLanguage", "en") # Default to English if not set

# Define the HTML code for the speech recognition interface
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the placeholder language with the setting from your .env
HtmlCode = HtmlCode.replace("recognition.lang", InputLanguage)

# Write the HTML file to the Data folder
voice_html_path = os.path.join(base_dir, "Data", "Voice.html")
os.makedirs(os.path.dirname(voice_html_path), exist_ok=True)
with open(voice_html_path, "w") as f:
    f.write(HtmlCode)

# --- SELENIUM SETUP ---
# Configure Chrome to run silently in the background
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Link to the generated HTML file
Link = f"file:///{voice_html_path.replace(os.sep, '/')}"

def SetAssistantStatus(Status):
    """Sets the assistant's status by writing it to a file"""
    status_path = os.path.join(base_dir, "Frontend", "Files", "Status.data")
    os.makedirs(os.path.dirname(status_path), exist_ok=True)
    with open(status_path, "w", encoding='utf-8') as f:
        f.write(Status)

def QueryModifier(Query):
    """Ensures proper punctuation and formatting"""
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which"]
    
    if any(word in new_query for word in question_words):
        if not new_query.endswith("?"):
            new_query += "?"
    else:
        if not new_query.endswith("."):
            new_query += "."
    
    return new_query.capitalize()

def UniversalTranslator(Text):
    """Translates text into English using mtranslate"""
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognition():
    """Performs speech recognition using the Selenium-driven browser"""
    driver.get(Link)
    driver.find_element(by=By.ID, value="start").click()
    
    while True:
        try:
            Text = driver.find_element(by=By.ID, value="output").text
            if Text:
                driver.find_element(by=By.ID, value="end").click()
                
                if InputLanguage.lower().startswith("en"):
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception:
            pass

# Main execution block
if __name__ == "__main__":
    while True:
        print("Listening...")
        text = SpeechRecognition()
        print(f"Recognized: {text}")