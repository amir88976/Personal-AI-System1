import os
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters
from openai import OpenAI

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

async def chat(update, context):
    text = update.message.text

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role":"user","content":text}
        ]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)


app = Application.builder().token(bot_token).build()

app.add_handler(
    MessageHandler(filters.TEXT, chat)
)

app.run_polling()
