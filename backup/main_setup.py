# ------------------------------------------------------------------

# IMPULSE BOT

# ------------------------------------------------------------------

# Imports
import os
import random
import asyncio
import platform
from pathlib import Path

# Third PArty Modules
import discord
import motor.motor_asyncio
from discord.ext import commands
from utils import json_loader
from utils.mongo import Document


# ---------------------------------------------------------------------

async def get_prefix(bot, message):
    # If DM
    if not message.guild:
        return commands.when_mentioned_or("!")(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or("!")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)

    except KeyError:
        return commands.when_mentioned_or("!")(bot, message)


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
bot.remove_command('help')

# Json
secret_file = json_loader.read_json("secrets")  # Secrets

# Json Variables
owner_id = secret_file["owner_id"]

# Define a few things...
choice = random.choice
randint = random.randint

python_version = platform.python_version()
discord_py_version = discord.__version__

# Colors
bot.colors = {
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x71368A,
    'DARK_VIVID_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_NAVY': 0x2C3E50
}

bot.color_list = [c for c in bot.colors.values()]

# Bot Object Variables
bot.version = "1.4.5"
bot.date = "4th October 2020"
bot.blacklisted_users = []
bot.config_token = secret_file["token"]
bot.connection_url = secret_file["mongo"]

# Current Working Directory
cwd = Path(__file__).parents[0]
cwd = str(cwd)


# ---------------------------------------------------------------------

@bot.event
async def on_ready():
    # To let cogs load
    await asyncio.sleep(0.5)

    print(f'Logged in as: {bot.user.name}\n---------')
    print(f'Id: {bot.user.id}\n---------')
    print(f"Path: {cwd}\n---------")

    # Tasks
    bot.loop.create_task(change_status())

    # DB
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["impulse"]
    bot.config = Document(bot.db, "config")
    print("Initialized Database\n-----")

    for document in await bot.config.get_all():
        print(document)


# ----------------------------------------------------------------------------

# Change Status
async def change_status():
    await bot.wait_until_ready()

    # Local Variables
    statuses = [f"| By Kwuartz_", f"| -help", f"| {str(len(bot.guilds))} Servers!"]
    statusnum = 0
    statuslen = len(statuses)

    # Loop
    while not bot.is_closed():

        # StatusNumChanger
        if statusnum == statuslen:
            statusnum = 0

        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=statuses[statusnum]))
        await asyncio.sleep(5)

        statusnum = statusnum + 1


# -------------------------------------------------------------------------

print("All cogs have been succesfully loaded and will be online shortly\n")


# ---------------------------------------------------------------------------

# Commands in testing

# BotInfo
@bot.command(aliases=["info", "statistics", "botinfo"], description="Shows bot info.")
async def stats(ctx):
    embed = discord.Embed(colour=random.choice(bot.color_list), timestamp=ctx.message.created_at)

    embed.add_field(name="**Owner:**", value=f"``Kwuartz#5106``")
    embed.add_field(name="**Servers:**", value=f"``{len(bot.guilds)} Servers``")
    embed.add_field(name="**Version:**", value=f"``{bot.version}``")
    embed.add_field(name="**Date of Creation:**", value=f"``{bot.date}``")
    embed.add_field(name="**Python Version:**", value=f"``{python_version}``")
    embed.add_field(name="**Discord.py Version**", value=f"``{discord_py_version}``")

    embed.set_author(name="Bot Stats", icon_url=bot.user.avatar_url)
    embed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=embed)


# Help
@bot.command()
async def help(ctx):
    embed = discord.Embed(colour=random.choice(bot.color_list), timestamp=ctx.message.created_at)
    embed.title = "**Commands:**"
    embed.description = f"**General Commands:**\n``-help`` - The command you are looking at.\n``-colourgen`` - Gives you a random coulour.\n``-ping`` - Checks your latency.\n``-info`` - Tells you more about the **Impulse** bot.\n``-echo [text]`` - Repeats what you tell the bot to repeat.\n``-setprefix [new prefix]`` - Changes the prefix for this bot.\n``-coinflip [player1choice] [player2choice]`` - Flips a coin.\n``-randomnum [startnumber] [endnumber]`` - Gives you a random number.\n\n**Fun Commands:**\n``-penguin`` - Shows you a cute penguin!\n``-animal`` - Shows you a random animal. \n``-spamping [victim] [amount]`` - Spam ping a victim of your choice.\n``-faker`` - League of Lengends Reference.\n``-8ball [question]`` - Answers a question for you.\n\n**Moderation Commands:**\n``-clear [amount]`` - Clears a certain amount of messages.\n``-kick [user]`` - Kicks a user.\n``-ban [user] [reason(optional)]`` - Bans a user.\n``-mute [user]`` - Mutes a user.\n``-unmute [user]`` - unmutes a user."
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.author.id in bot.blacklisted_users:
        return


if __name__ == '__main__':
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)
