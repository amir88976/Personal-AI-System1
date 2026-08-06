import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from groq import Groq


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

client = Groq(api_key=GROQ_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋 من دستیار هوش مصنوعی تو هستم."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    result = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "تو یک دستیار فارسی زبان باهوش هستی."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    answer = result.choices[0].message.content

    await update.message.reply_text(answer)


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT, chat)
)

print("Bot is running...")

app.run_polling(
    close_loop=False
)
