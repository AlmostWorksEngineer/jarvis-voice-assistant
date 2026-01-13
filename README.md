# 🤖 JARVIS – Voice Controlled AI Assistant (Iron Man Inspired)

JARVIS is a real-time voice-controlled desktop assistant inspired by Iron Man’s AI.
Built using Python, it listens for a wake word, understands multiple commands, controls your system, reads on-screen text, and replies with a natural AI voice.

This project demonstrates AI interaction, automation, system control, and speech technologies in a single integrated system.

---

## 🚀 Features

- 🎙 Wake-word detection (“Hey Jarvis”)
- 🧠 Execute multiple commands in one sentence
- 🗣 Natural voice replies (Microsoft Edge Neural TTS)
- 👁 Read selected on-screen text
- ✂ Summarize selected text
- 🌐 Browser automation (Chrome, Google search)
- 🔊 System volume control
- 💡 Screen brightness control
- ▶ Media playback control
- 💬 Terminal displays everything Jarvis says
- 🔁 Continuous background listening (no restart required)

---

## 🧩 System Architecture

The assistant is divided into four logical components, inspired by Iron Man’s JARVIS:

| Component | Responsibility |
|---------|----------------|
| 👁 Eyes | Reads selected screen text |
| 👂 Ears | Listens to voice commands |
| 🧠 Brain | Processes logic and decisions |
| 👄 Mouth | Responds using AI voice |

---

## 🛠 Tech Stack

- Python 3.10+
- speechrecognition
- edge-tts
- pyautogui
- pyperclip
- playsound
- pycaw
- screen-brightness-control
- Windows COM Audio APIs

⚠️ Currently supports Windows OS only

---

## 📦 Installation

### 1️⃣ Clone the repository
git clone https://github.com/your-username/jarvis-ai.git
cd jarvis-ai


### 2️⃣ (Recommended) Create virtual environment
python -m venv venv
venv\Scripts\activate


### 3️⃣ Install dependencies
pip install -r requirements.txt

---

## ▶️ Running Jarvis

python jarvis.py


Jarvis will say:
Jarvis online. Say 'Hey Jarvis' to begin.


---

## 🎤 Example Voice Commands

"Hey Jarvis
open chrome and increase volume and search google for python tutorials"

"Hey Jarvis read this"



---

## 📋 Supported Commands

| Command | Action |
|-------|--------|
| Open Chrome | Launch browser |
| Search Google for X | Web search |
| Increase / Decrease volume | Audio control |
| Mute / Unmute volume | Audio control |
| Set brightness 50 | Screen brightness |
| Play / Pause music | Media control |
| Read this | Reads selected text |
| Summarize this | Summarizes text |
| Stop Jarvis | Exit program |

---

## ⚠️ Known Limitations

- Speech recognition requires internet
- Wake-word accuracy depends on microphone quality
- Optimized for Windows only

---

## 🔮 Future Enhancements

- Offline AI model integration
- HUD-style GUI (Iron Man style)
- Contextual memory
- Cross-platform support
- Smarter intent recognition

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Mridul Giri  
AI & Automation Engineering Project

If you find this project useful, ⭐ star the repository!

---

## 🧠 Educational Value

This project demonstrates:
- Human-Computer Interaction
- Speech Recognition
- Text-to-Speech Systems
- OS Automation
- AI System Design


### 1️⃣ Clone the repository
