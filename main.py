import os
import logging
import time
import pyttsx3
import pyautogui
import webbrowser
import subprocess
from dotenv import load_dotenv
import speech_recognition as sr
from langchain_ollama import ChatOllama, OllamaLLM

# from langchain_openai import ChatOpenAI # if you want to use openai
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# importing tools
from tools.time import get_time
from tools.OCR import read_text_from_latest_image
from tools.arp_scan import arp_scan_terminal
from tools.duckduckgo import duckduckgo_search_tool
from tools.matrix import matrix_mode
from tools.screenshot import take_screenshot
from langchain_core.tools import tool

@tool
def open_application_or_url(query: str) -> str:
    """Открывает любую программу или сайт. Примеры: github, steam, telegram, minecraft, discord, notepad"""
    query = query.lower().strip()
    
    apps = {
        "github": "https://github.com",
        "git hub": "https://github.com",
        "гитхаб": "https://github.com",
        "steam": "steam://",
        "стим": "steam://",
        "telegram": "tg://",
        "телеграм": "tg://",
        "minecraft": "minecraft",
        "майнкрафт": "minecraft",
        "майн": "minecraft",
        "discord": "discord",
        "дискорд": "discord",
        "notepad": "notepad",
        "блокнот": "notepad",
        "vscode": "code",
        "code": "code",
        "браузер": "https://google.com",
        "chrome": "chrome",
        "хром": "chrome",
    }
    
    for key, value in apps.items():
        if key in query:
            if value.startswith("http"):
                webbrowser.open(value)
                return f"Открываю {key} в браузере"
            elif value.endswith("://"):
                webbrowser.open(value)
                return f"Запускаю {key}"
            else:
                try:
                    subprocess.Popen(value)
                    return f"Запускаю {key}"
                except:
                    pyautogui.hotkey('win', 'r')
                    pyautogui.typewrite(value)
                    pyautogui.press('enter')
                    return f"Открываю {key} через Win+R"
    
    # Если ничего не нашёл — просто Win+R
    pyautogui.hotkey('win', 'r')
    pyautogui.typewrite(query)
    pyautogui.press('enter')
    return f"Пытаюсь открыть: {query}"

load_dotenv()

MIC_INDEX = None
TRIGGER_WORD = "jarvis"
CONVERSATION_TIMEOUT = 30  # seconds of inactivity before exiting conversation mode

logging.basicConfig(level=logging.DEBUG)  # logging

# api_key = os.getenv("OPENAI_API_KEY") removed because it's not needed for ollama
# org_id = os.getenv("OPENAI_ORG_ID") removed because it's not needed for ollama

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=MIC_INDEX)

# Initialize LLM
llm = ChatOllama(model="llama3.2:3b", temperature=0.7)

# llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, organization=org_id) for openai

# Tool list
tools = [get_time, arp_scan_terminal, read_text_from_latest_image, duckduckgo_search_tool, matrix_mode, take_screenshot, open_application_or_url]

# Tool-calling prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are Jarvis, an intelligent, conversational AI assistant. Your goal is to be helpful, friendly, and informative. You can respond in natural, human-like language and use tools when needed to answer questions more accurately. Always explain your reasoning simply when appropriate, and keep your responses conversational and concise.",
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# TTS setup
def speak_text(text: str):
    try:
        engine = pyttsx3.init()
        for voice in engine.getProperty("voices"):
            if "jamie" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break
        engine.setProperty("rate", 180)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.3)
    except Exception as e:
        logging.error(f"❌ TTS failed: {e}")


# Main interaction loop
def write():
    conversation_mode = False
    last_interaction_time = None

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    if not conversation_mode:
                        logging.info("🎤 Listening for wake word...")
                        audio = recognizer.listen(source, timeout=10)
                        transcript = recognizer.recognize_google(audio)
                        logging.info(f"🗣 Heard: {transcript}")

                        if TRIGGER_WORD.lower() in transcript.lower():
                            logging.info(f"🗣 Triggered by: {transcript}")
                            speak_text("Yes sir?")
                            conversation_mode = True
                            last_interaction_time = time.time()
                        else:
                            logging.debug("Wake word not detected, continuing...")
                    else:
                        logging.info("🎤 Listening for next command...")
                        audio = recognizer.listen(source, timeout=10)
                        command = recognizer.recognize_google(audio)
                        logging.info(f"📥 Command: {command}")

                        logging.info("🤖 Sending command to agent...")
                        response = executor.invoke({"input": command})
                        content = response["output"]
                        logging.info(f"✅ Agent responded: {content}")

                        print("Jarvis:", content)
                        speak_text(content)
                        last_interaction_time = time.time()

                        if time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                            logging.info("⌛ Timeout: Returning to wake word mode.")
                            conversation_mode = False

                except sr.WaitTimeoutError:
                    logging.warning("⚠️ Timeout waiting for audio.")
                    if (
                        conversation_mode
                        and time.time() - last_interaction_time > CONVERSATION_TIMEOUT
                    ):
                        logging.info(
                            "⌛ No input in conversation mode. Returning to wake word mode."
                        )
                        conversation_mode = False
                except sr.UnknownValueError:
                    logging.warning("⚠️ Could not understand audio.")
                except Exception as e:
                    logging.error(f"❌ Error during recognition or tool call: {e}")
                    time.sleep(1)

    except Exception as e:
        logging.critical(f"❌ Critical error in main loop: {e}")



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="JARVIS — голосовой или текстовый режим")
    parser.add_argument("--text", action="store_true", help="Запуск в текстовом режиме (без микрофона)")
    args = parser.parse_args()

    if args.text:
        print("JARVIS — ТЕКСТОВЫЙ РЕЖИМ (STELS). Пиши команды, 'exit' — выход")
        while True:
            try:
                command = input("\nТы → ").strip()
                if command.lower() in ["exit", "выход", "quit", "пока"]:
                    print("JARVIS выключен.")
                    break
                if not command:
                    continue

                print("JARVIS думает...")
                response = executor.invoke({"input": command})
                answer = response["output"]
                print(f"JARVIS → {answer}")

            except KeyboardInterrupt:
                print("\nJARVIS выключен.")
                break
            except Exception as e:
                print(f"Ошибка: {e}")

    else:
        print("JARVIS — ГОЛОСОВОЙ РЕЖИМ активирован. Скажи 'Jarvis'...")
        write()  # ← твоя оригинальная голосовая функция остаётся нетронутой