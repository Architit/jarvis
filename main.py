import os
import logging
import time
import pyttsx3
import pyautogui
import webbrowser
import subprocess
import pyperclip # НУЖЕН ДЛЯ ВСТАВКИ ТЕКСТА (ОБХОД РАСКЛАДКИ)
from dotenv import load_dotenv
import speech_recognition as sr

from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType, Tool

logging.basicConfig(level=logging.INFO, format="%(message)s")
load_dotenv()

# --- УМНЫЙ ЗАПУСК (НЕ ЗАВИСИТ ОТ РАСКЛАДКИ) ---
def open_app_function(query: str) -> str:
    """Открывает приложения через Win+R с использованием буфера обмена."""
    query = query.lower().strip()
    target = query
    
    # Маппинг для удобства
    if "калькулятор" in query or "calc" in query: target = "calc.exe"
    elif "блокнот" in query or "notepad" in query: target = "notepad.exe"
    elif "cmd" in query or "терминал" in query: target = "cmd.exe"
    elif "браузер" in query or "хром" in query: target = "https://google.com"
    elif "steam" in query: target = "steam"

    print(f"🔧 JARVIS TOOL: Пытаюсь открыть '{target}'...")

    # 1. Попытка системного запуска (самая надежная, вообще без мыши)
    try:
        # Для Windows
        subprocess.Popen(f'start "" "{target}"', shell=True)
        return f"Запущено через Shell: {target}"
    except Exception as e:
        print(f"⚠️ Shell не сработал: {e}. Пробую метод Win+R (Paste)...")

    # 2. Метод Win+R через Ctrl+V (Работает с ЛЮБОЙ раскладкой)
    try:
        pyautogui.hotkey("win", "r")
        time.sleep(0.5) # Ждем окно
        
        # КОПИРУЕМ В БУФЕР И ВСТАВЛЯЕМ (ОБХОД РАСКЛАДКИ)
        pyperclip.copy(target) 
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.1)
        
        pyautogui.press("enter")
        return f"Запущено через Win+R: {target}"
    except Exception as e:
        return f"Ошибка запуска: {e}"

tools = [
    Tool(
        name="OpenApplication",
        func=open_app_function,
        description="Открывает программы или сайты. Принимает имя (calc, notepad, google.com)."
    )
]

print("🧠 Инициализация Ollama (llama3.2:3b)...")
llm = ChatOllama(model="llama3.2:3b", temperature=0)

print("🤖 Создание Агента...")
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

def speak_text(text: str):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        pass

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", action="store_true", help="Текстовый режим")
    args = parser.parse_args()

    print("\n" + "="*40)
    print("   JARVIS (LAYOUT INDEPENDENT) ГОТОВ")
    print("="*40 + "\n")

    if args.text:
        print("📝 РЕЖИМ: ТЕКСТ (пиши 'exit' для выхода)")
        while True:
            try:
                user_input = input("\nТы → ").strip()
                if not user_input: continue
                if user_input.lower() in ["exit", "выход"]: break

                response = agent_executor.run(user_input)
                print(f"🤖 Jarvis: {response}")
                
            except Exception as e:
                print(f"❌ Ошибка: {e}")
    else:
        print("🎤 РЕЖИМ: ГОЛОС")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            while True:
                try:
                    print("Слушаю...")
                    audio = r.listen(source, timeout=5)
                    text = r.recognize_google(audio, language="ru-RU")
                    print(f"Вы сказали: {text}")
                    if "jarvis" in text.lower() or "джарвис" in text.lower():
                        response = agent_executor.run(text)
                        speak_text(response)
                except Exception as e:
                    pass
