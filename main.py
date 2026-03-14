import discord
import os
import google.generativeai as genai
from discord.ext import commands

# Environment variables
TOKEN = os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# AI model
model = genai.GenerativeModel("gemini-2.5-flash")

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    user_message = message.content

    try:
        response = model.generate_content(user_message)
        reply = response.text
    except Exception as e:
        print(e)
        reply = "AI cannot respond right now."

    if len(reply) > 1900:
        reply = reply[:1900]

    await message.channel.send(reply)


bot.run(TOKEN)
