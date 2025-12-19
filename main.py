import logging
import asyncio
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ChatJoinRequestHandler, ContextTypes

# --- 1. APNI DETAILS BHARO ---
BOT_TOKEN = "8348595037:AAEFb9mol2REAkMv2bxhdoWzXXh_0uU70Cs"
CHANNEL_ID = -1003461333677  # Channel ID
CHANNEL_LINK = "https://t.me/+woM14Wt4pFI3NTg1" # Request wala link
DIRECT_LINK = "https://t.me/+ZovlP8fgbwQ4YTZl" # Channel ka main link
# -----------------------------

# --- 2. 24/7 SERVER SETUP (FLASK) ---
app = Flask('')

@app.route('/')
def home():
    return "I am Alive! Bot chal raha hai."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------------------

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    keyboard = [[InlineKeyboardButton("🎬 JOIN CHANNEL TO WATCH", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Hello {user_first_name}! 👋\n\nMovies dekhne ke liye pehle Channel Join karein.\nNiche button dabayein, request auto accept ho jayegi! 👇",
        reply_markup=reply_markup
    )

async def auto_accept(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.chat_join_request.from_user.id
    chat_id = update.chat_join_request.chat.id
    try:
        await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
    except:
        return

    # 3 Second Delay
    await asyncio.sleep(3)

    try:
        keyboard = [[InlineKeyboardButton("🍿 https://t.me/+ZovlP8fgbwQ4YTZl", url=DIRECT_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=user_id,
            text="✅ **Request Accepted!**\n\nAb aap saari Movies dekh sakte hain. Jaldi aao! 👇",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except:
        pass

def main():
    # Pehle Server start karo
    keep_alive()
    # Phir Bot start karo
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(ChatJoinRequestHandler(auto_accept))
    application.run_polling()

if __name__ == "__main__":
    main()
