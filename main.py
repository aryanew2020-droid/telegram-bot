# main.py
from flask import Flask
from threading import Thread
from telegram.ext import Updater, CommandHandler
import os

# Flask webserver (for UptimeRobot ping)
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Bot logic
def start(update, context):
    update.message.reply_text("Hello bhai! Main zinda hoon 🚀")

def help_command(update, context):
    update.message.reply_text("Commands:\n/start - Greet\n/help - Help menu")

def run_bot():
    TOKEN = os.environ.get("8225064493:AAEyCw-j661DrYOD3ZraosTDYBYaAZ2-pug")  # get from Replit Secrets
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    # Run web + bot in parallel
    Thread(target=run_web).start()
    run_bot()
