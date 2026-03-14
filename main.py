import discord
from discord.ext import commands
import requests
import os

TOKEN = os.getenv("TOKEN")
AI_KEY = os.getenv("AI_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def ask_ai(question):

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    headers = {
        "Authorization": f"Bearer {AI_KEY}"
    }

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=data,
        headers=headers
    )

    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]

    return "I cannot answer right now."


@bot.event
async def on_ready():
    print("Bot is online")


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    question = message.content

    answer = ask_ai(question)

    if len(answer) > 1900:
        answer = answer[:1900]

    await message.channel.send(answer)


bot.run(TOKEN)
