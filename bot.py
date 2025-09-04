from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("8225064493:AAEyCw-j661DrYOD3ZraosTDYBYaAZ2-pug")  


paid_members = "@ajay8630033"  

UPI_LINK = "upi://pay?pa=nakuldev34567@ybl&pn=NakulDev&am=199&cu=INR"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! ✅ Free features unlocked.\n\n"
        "For NSFW premium, please pay here:\n"
        f"{UPI_LINK}\n\n"
        "After payment, send screenshot to admin 📸"
    )

async def sfw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here’s a safe meme for everyone 🌸")

async def nsfw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in paid_members:
        await update.message.reply_text("🔥 NSFW content for members only 🔥")
    else:
        await update.message.reply_text(
            "❌ This is premium. Please pay first:\n" + UPI_LINK
        )

app = ApplicationBuilder().token(8225064493:AAEyCw-j661DrYOD3ZraosTDYBYaAZ2-pug).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("sfw", sfw))
app.add_handler(CommandHandler("nsfw", nsfw))

app.run_polling()
