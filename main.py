import os
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


client = OpenAI(
    api_key=AI_KEY
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 دستیار هوش مصنوعی آنلاین شد."
    )


def ask_ai(message):

    try:
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "تو یک دستیار هوش مصنوعی حرفه‌ای هستی. "
                    "فارسی جواب بده و دقیق کمک کن."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return result.choices[0].message.content


    except Exception as e:
        return "خطا در ارتباط با هوش مصنوعی: " + str(e)



async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    await update.message.reply_text(
        "⏳ دارم فکر می‌کنم..."
    )

    answer = ask_ai(user_text)

    await update.message.reply_text(answer)



def main():

    if not BOT_TOKEN:
        print("BOT_TOKEN missing")
        return

    app = Application.builder().token(
        BOT_TOKEN
    ).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )


    print("AI BOT STARTED")

    app.run_polling()



if __name__ == "__main__":
    main()
