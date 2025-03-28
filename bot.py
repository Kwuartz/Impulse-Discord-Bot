# Standard libraries
import asyncio
import os
import logging

# Third party libraries
import discord
from pathlib import Path
import motor.motor_asyncio
from discord.ext import commands

# Local Modules
import utils.json_loader
from utils.mongo import Document

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


async def get_prefix(bot, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or("-")(bot, message)

    try:
        data = await bot.prefixes.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or("-")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)

    except:
        return commands.when_mentioned_or("-")(bot, message)

# Defining a few things
secret_file = utils.json_loader.read_json('secrets')
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
bot.config_token = secret_file["token"]
bot.connection_url = secret_file["mongo"]
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.cwd = cwd

bot.version = "10"

bot.colors = {
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xe74c3c,
    "DARK_AQUA": 0x11806A,
    "DARK_GREEN": 0x1F8B4C,
    "DARK_BLUE": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "DARK_ORANGE": 0xA84300,
    "DARK_RED": 0x992D22,
}

bot.color_list = [c for c in bot.colors.values()]
bot.remove_command('help')


@bot.command()
async def test(ctx):
    await ctx.send("test")


@bot.event
async def on_ready():
    # To let cogs load
    await asyncio.sleep(0.5)

    print(f'Logged in as: {bot.user.name}\n---------')
    print(f'Id: {bot.user.id}\n---------')
    print(f"Path: {cwd}\n---------")

    # Tasks
    bot.loop.create_task(change_status())

    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["impulse"]
    bot.prefixes = Document(bot.db, "prefix")
    bot.blacklist = Document(bot.db, "blacklist")
    bot.automod = Document(bot.db, "automod")
    bot.exp = Document(bot.db, "exp")

    blacklisted = await get_blacklisted_users()

    for user in blacklisted:
        bot.blacklisted_users.append(user)

    print("Initialized Database\n-----")


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


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id in bot.blacklisted_users:
        await message.channel.send(f"You have been blacklisted {message.author.mention}!", delete_after=5)
        return

    await bot.process_commands(message)



# --------------------------------------------------------------------------------

# Functions
async def get_blacklisted_users():
    users = await bot.blacklist.get_all()
    blacklisted_users = []

    for user in users:
        blacklisted_users.append(user["_id"])

    return blacklisted_users


# ------------------------------------------------------------------------------------

# Start Bot If Main File

if __name__ == "__main__":
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(bot.config_token)
