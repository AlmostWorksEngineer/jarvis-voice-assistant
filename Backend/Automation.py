# ===============================
# Import required libraries
# ===============================

from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import urllib.parse
import os
import sys
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

load_dotenv(os.path.join(base_path, ".env"))


from dotenv import dotenv_values

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(BASE_DIR, ".env"))

GroqAPIKey = env_vars.get("GroqAPIKey")

if not GroqAPIKey:
    raise RuntimeError("GroqAPIKey NOT loaded. Check .env path.")


# ===============================
# User-Agent
# ===============================

useragent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/100.0.4896.75 Safari/537.36"
)

# ===============================
# Google Search
# ===============================

def GoogleSearch(topic):
    query = urllib.parse.quote_plus(topic)
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(url)
    return True


# ===============================
# YouTube
# ===============================

def YouTubeSearch(topic):
    query = urllib.parse.quote_plus(topic)
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return True


def PlayYoutube(query):
    playonyt(query)
    return True

import urllib.parse
import webbrowser

def WriteGmail(to, subject, body):
    to = urllib.parse.quote(to)
    subject = urllib.parse.quote(subject)
    body = urllib.parse.quote(body)

    url = (
        "https://mail.google.com/mail/?view=cm&fs=1"
        f"&to={to}&su={subject}&body={body}"
    )

    webbrowser.open(url)
    return True



# ===============================
# App Open / Close
# ===============================

import re

def OpenApp(app, sess=requests.session()):
    app = app.lower().strip()

    # 🌐 DIRECT WEBSITE (github.com, xyz.in, etc.)
    if re.search(r"\.(com|org|net|in|io|ai|edu)$", app):
        if not app.startswith("http"):
            app = "https://" + app
        webbrowser.open(app)
        return True

    # 📧 EMAIL
    if "email" in app or "mail" in app or "gmail" in app:
        webbrowser.open("https://mail.google.com/")
        return True

    # 🌐 COMMON SITES
    if "youtube" in app:
        webbrowser.open("https://www.youtube.com")
        return True

    if "google" in app:
        webbrowser.open("https://www.google.com")
        return True

    # 🖥️ LOCAL APPLICATION
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True

    except Exception as e:
        print(f"[red]AppOpener failed:[/red] {e}")

        # 🔁 GOOGLE FALLBACK
        url = f"https://www.google.com/search?q={app}"
        webbrowser.open(url)
        return False


def CloseApp(app):
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False


# ===============================
# System Controls
# ===============================

def System(command):
    if command == "mute":
        keyboard.press_and_release("volume mute")
    elif command == "unmute":
        keyboard.press_and_release("volume mute")
    elif command == "volume up":
        keyboard.press_and_release("volume up")
    elif command == "volume down":
        keyboard.press_and_release("volume down")
    return True

def ParseEmailCommand(command: str):
    """
    Expected format:
    email to someone@gmail.com subject something body something else
    """
    command = command.replace("email ", "").strip()

    to = ""
    subject = ""
    body = ""

    if " to " in f" {command} ":
        to = command.split(" to ")[1].split(" subject ")[0].strip()

    if " subject " in f" {command} ":
        subject = command.split(" subject ")[1].split(" body ")[0].strip()

    if " body " in f" {command} ":
        body = command.split(" body ")[1].strip()

    return to, subject, body



# ===============================
# Async Command Translator
# ===============================

async def TranslateAndExecute(commands: list[str]):

    normalized_commands = []

    # ===============================
    # NORMALIZATION PHASE
    # ===============================
    for command in commands:
        cmd = command.lower()
        
    # 📧 EMAIL OVERRIDE
        if cmd in ["open email", "open email application", "email"]:
            normalized_commands.append("send email")
            continue


        # 📧 EMAIL SHOULD NEVER TURN INTO GOOGLE SEARCH
        if cmd.startswith("send email"):
            normalized_commands.append(command)
            continue

        # 🎵 PLAY HAS PRIORITY
        if cmd.startswith("general play "):
            normalized_commands.append(
                "play " + command.replace("general play ", "")
            )

        elif cmd.startswith("play "):
            normalized_commands.append(command)

        # 🔍 GENERAL → GOOGLE SEARCH
        elif cmd.startswith("general "):
            normalized_commands.append(
                "google search " + command.replace("general ", "")
            )

        elif cmd.startswith("realtime search "):
            normalized_commands.append(
                "google search " + command.replace("realtime search ", "")
            )

        elif cmd.startswith("search "):
            normalized_commands.append(
                "google search " + command.replace("search ", "")
            )

        else:
            normalized_commands.append(command)

    # ===============================
    # EXECUTION PHASE
    # ===============================
    funcs = []

    for command in normalized_commands:

        if command.startswith("play "):
            funcs.append(
                asyncio.to_thread(
                    PlayYoutube,
                    command.replace("play ", "")
                )
            )

        elif command.startswith("youtube search "):
            funcs.append(
                asyncio.to_thread(
                    YouTubeSearch,
                    command.replace("youtube search ", "")
                )
            )

        elif command.startswith("google search "):
            funcs.append(
                asyncio.to_thread(
                    GoogleSearch,
                    command.replace("google search ", "")
                )
            )

        elif command.startswith("send email"):
            to, subject, body = ParseEmailCommand(command)

            funcs.append(
                asyncio.to_thread(
                    WriteGmail,
                    to,
                    subject,
                    body
                )
            )

        elif command.startswith("open "):
            funcs.append(
                asyncio.to_thread(
                    OpenApp,
                    command.replace("open ", "")
                )
            )

        elif command.startswith("close "):
            funcs.append(
                asyncio.to_thread(
                    CloseApp,
                    command.replace("close ", "")
                )
            )

        elif command.startswith("system "):
            funcs.append(
                asyncio.to_thread(
                    System,
                    command.replace("system ", "")
                )
            )

        else:
            print(f"No Function Found For {command}")

    await asyncio.gather(*funcs)
    return True



# ===============================
# Automation Entry
# ===============================

async def Automation(commands: list[str]):
    await TranslateAndExecute(commands)
    return True
