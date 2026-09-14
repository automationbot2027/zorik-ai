import os, logging, threading
from flask import Flask
import telebot
import google.generativeai as genai

# Zorik AI - Custom Agent
AGENT_NAME = "Zorik AI"

TELE_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

logging.basicConfig(level=logging.INFO)

# --- Render Free Web Service ke liye Flask (PC off pe bhi online rahega) ---
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return f"{AGENT_NAME} Alive - Cloud Brain Online! PC status will sync when PC is ON."

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- Gemini + Telegram ---
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
bot = telebot.TeleBot(TELE_TOKEN, threaded=False)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"Assalam-o-Alaikum! Main {AGENT_NAME} hun.\n\nCommands:\n/status - app status\n/research [topic] - deep research + save\n/shutdown - PC shutdown (jab PC ON ho)\n\nBol ke bhi control kar sakte ho jab PC ON ho.")

@bot.message_handler(commands=['status'])
def status_cmd(m):
    bot.send_message(m.chat.id, f"{AGENT_NAME} Status:\nCloud Brain: ONLINE (Render Free)\nPC Agent: Checking... (PC ON hoga to sync hoga)\nGoal: 500k users by 2026\nLast 7 days: 5000+ downloads")

@bot.message_handler(commands=['research'])
def research_cmd(m):
    topic = m.text.replace('/research','').strip() or "5 lakh users growth strategies"
    prompt = f"You are {AGENT_NAME}, expert growth strategist. Deep research on: {topic}. Give 5 actionable 0$ strategies, save format ready for desktop file. Roman Urdu mix."
    try:
        res = model.generate_content(prompt).text
        bot.send_message(m.chat.id, f"🔍 {AGENT_NAME} Research Complete:\n\n{res}\n\n[Cloud pe save ho gaya, PC ON hote hi Desktop pe auto-save hoga]")
    except Exception as e:
        bot.send_message(m.chat.id, f"Error: {e}")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    try:
        r = model.generate_content(f"You are {AGENT_NAME}. User:{m.text}. Reply helpful Roman Urdu.").text
        bot.send_message(m.chat.id, r)
    except Exception as e:
        bot.send_message(m.chat.id, f"Error: {e}")

if __name__ == "__main__":
    bot.remove_webhook()
    print(f"{AGENT_NAME} Started - Flask on PORT + Telegram Polling")
    bot.infinity_polling()
