import os, logging, threading, time
from flask import Flask
import telebot
import google.generativeai as genai
from flask import request, jsonify

AGENT_NAME = "Zorik AI"
TELE_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

logging.basicConfig(level=logging.INFO)
flask_app = Flask(__name__)

@flask_app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response
@flask_app.route('/')
def home():
    return f"{AGENT_NAME} Alive - Cloud Brain Online! PC OFF pe bhi online."

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
bot = telebot.TeleBot(TELE_TOKEN, threaded=False)

@bot.message_handler(commands=['start'])
def start(m):
    try:
        bot.reply_to(m, f"Assalam-o-Alaikum! Main {AGENT_NAME} hun.\n\nCommands:\n/status - app status\n/research [topic] - deep research + save\n/shutdown - PC shutdown (jab PC ON ho)\n\nBol ke bhi control kar sakte ho jab PC ON ho.")
    except Exception as e: print(e)

@bot.message_handler(commands=['status'])
def status_cmd(m):
    try:
        bot.reply_to(m, f"{AGENT_NAME} Status:\nCloud Brain: ONLINE ✅ (Render Free)\nPC Agent: OFF - Jab PC ON karoge to sync hoga\nGoal: 500k users by 2026\nLast 7 days: 5000+ downloads - 6 month target")
    except Exception as e: print(f"Status err: {e}")

@bot.message_handler(commands=['research'])
def research_cmd(m):
    topic = m.text.replace('/research','').strip() or "5 lakh users growth"
    try:
        res = model.generate_content(f"You are {AGENT_NAME}. Deep research on {topic} in Roman Urdu, 5 points, 0$ budget.").text
        bot.reply_to(m, f"🔍 {AGENT_NAME} Research:\n\n{res[:4000]}")
    except Exception as e: bot.reply_to(m, f"Research Error: {e}")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    try:
        r = model.generate_content(f"You are {AGENT_NAME}. User:{m.text}. Reply Roman Urdu helpful.").text
        bot.reply_to(m, r[:4000])
    except Exception as e: bot.reply_to(m, f"Error: {e}")

if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(2)
    print(f"{AGENT_NAME} Started")
    while True:
        try: bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e: print(f"Polling restart: {e}"); time.sleep(5)

@flask_app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    ai_response = model.generate_content(user_message)
    return jsonify({'response': ai_response.text})
