import os
import asyncio

from flask import Flask, request
from dotenv import load_dotenv

from openai import OpenAI

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("AI_KEY")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


client = OpenAI(
    api_key=AI_KEY
)


app = Flask(__name__)


telegram_app = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋 من آنلاینم. با من صحبت کن."
    )


def ask_ai(text):

    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content":
                "تو یک دستیار هوش مصنوعی فارسی زبان هستی. "
                "جواب‌های دقیق و مفید بده."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return result.choices[0].message.content


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    try:
        answer = ask_ai(text)
        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            "خطا: " + str(e)
        )


telegram_app.add_handler(
    CommandHandler("start", start)
)

telegram_app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        chat
    )
)


@app.route("/", methods=["GET"])
def home():
    return "AI Telegram Bot is running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True)

    update = Update.de_json(
        data,
        telegram_app.bot
    )

    asyncio.run(
        telegram_app.process_update(update)
    )

    return "ok"


@app.route("/set-webhook")
def set_webhook():

    asyncio.run(
        telegram_app.bot.set_webhook(
            WEBHOOK_URL + "/webhook"
        )
    )

    return "Webhook set"


if __name__ == "__main__":
    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
