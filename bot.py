import logging
import sqlite3
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# ---------------- CONFIG ----------------
TELEGRAM_TOKEN = os.getenv("8225064493:AAEyCw-j661DrYOD3ZraosTDYBYaAZ2-pug")
PERPLEXITY_API_KEY = os.getenv("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")  # instead of OPENAI
FREE_LIMIT = 3
UPI_ID = os.getenv("UPI_ID", "nakuldev34567@ybl")  # set your UPI here

# ---------------- LOGGING ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS users
       (user_id INTEGER PRIMARY KEY, requests INTEGER DEFAULT 0, premium INTEGER DEFAULT 0, last_request TEXT)"""
)
conn.commit()


def check_user(user_id):
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    today = datetime.now().date()
    if not user:
        c.execute("INSERT INTO users (user_id, last_request) VALUES (?, ?)", (user_id, str(today)))
        conn.commit()
        return (0, 0)
    last_request_date = datetime.strptime(user[3], "%Y-%m-%d").date() if user[3] else today
    if last_request_date < today:
        c.execute("UPDATE users SET requests = 0, last_request = ? WHERE user_id=?", (str(today), user_id))
        conn.commit()
        return (0, user[2])
    return (user[1], user[2])


def increment_requests(user_id):
    c.execute("UPDATE users SET requests = requests + 1 WHERE user_id=?", (user_id,))
    conn.commit()


def upgrade_premium(user_id):
    c.execute("UPDATE users SET premium = 1 WHERE user_id=?", (user_id,))
    conn.commit()


# ---------------- AI (Perplexity) ----------------
def ask_ai(prompt: str) -> str:
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "model": "sonar-pro",  # Perplexity main model
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {e}"


# ---------------- COMMANDS ----------------
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(
        f"Hello {user.first_name}! 👋\n\n"
        "I’m your AI Assistant powered by Perplexity 🤖\n"
        f"You have {FREE_LIMIT} free requests per day.\n"
        "👉 Use /buy to upgrade to Premium (Unlimited).\n"
    )


def buy(update: Update, context: CallbackContext):
    update.message.reply_text(
        "💎 Premium Plan:\n\n"
        "📌 Pay ₹199 via UPI\n"
        f"➡️ Send to: `{UPI_ID}`\n\n"
        "⚡ After payment, send `/paid <transaction_id>` to confirm.\n"
        "✅ You’ll be upgraded to Premium once verified."
    )


def paid(update: Update, context: CallbackContext):
    """User submits transaction ID after UPI payment"""
    user_id = update.effective_user.id
    if len(context.args) < 1:
        update.message.reply_text("⚠️ Please provide your transaction ID.\nExample: `/paid 123456`")
        return
    txn_id = context.args[0]
    # In real life → verify txn_id with Razorpay/UPI API
    upgrade_premium(user_id)
    update.message.reply_text(f"✅ Payment confirmed! Txn ID: {txn_id}\n🚀 You are now Premium.")


def chat(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    requests, premium = check_user(user_id)

    if requests >= FREE_LIMIT and not premium:
        update.message.reply_text(
            f"⚠️ You used your {FREE_LIMIT} free requests today.\n"
            "👉 Use /buy to upgrade to Premium 💎"
        )
        return

    prompt = update.message.text
    reply = ask_ai(prompt)
    increment_requests(user_id)
    update.message.reply_text(reply)


# ---------------- MAIN ----------------
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("buy", buy))
    dp.add_handler(CommandHandler("paid", paid))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
