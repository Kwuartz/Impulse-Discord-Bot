import discord
from discord.ext import commands
import random
import datetime

from utils import json_loader, lists


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events have been loaded\n-----")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='Welcome')

        if channel:
            embed = discord.Embed(description='Welcome to our guild!', color=random.choice(self.bot.color_list))
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='goodbye')

        if channel:
            embed = discord.Embed(description='Goodbye from all of us..', color=random.choice(self.bot.color_list))
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return

        elif message.author.id in self.bot.blacklisted_users:
            return

        if message.guild is not None:
            user = await self.bot.exp.find(message.author.id)

            if user is not None:
                userlevel = int(user["level"])
                userexp = int(user["exp"])

                userlevel_threshold = 5 * (userlevel ^ 2) + 50 * userlevel + 100

                if userexp > userlevel_threshold:
                    userlevel += 1
                    userexp = 0
                    await self.bot.exp.update({"_id": message.author.id, "level":  userlevel, "exp": userexp})

                await self.bot.exp.upsert({"_id": message.author.id, "level":  userlevel, "exp": userexp + 1})

            else:
                await self.bot.exp.insert({"_id": message.author.id, "level": 0, "exp": 0})

        try:
            automod = await self.bot.automod.find(message.guild.id)
            if automod["enabled"] is True:
                for word in lists.bad_words:
                    if message.content.lower().count(word) > 0:
                        embed = discord.Embed(colour=random.choice(self.bot.color_list))
                        embed.title = "**Auto Mod:**"
                        embed.description = f"{message.author.mention} **NO** Big Boy Words!"
                        embed.set_footer(text="Toggle Auto Mod OFF and ON with -auto",
                                         icon_url=message.author.avatar_url)
                        await message.channel.send(embed=embed, delete_after=5)
                        await message.delete()

        # Adds Guild to json if not in it!
        except:
            await self.bot.automod.upsert({"_id": message.guild.id, "enabled": False})
            words = ["Fuck", "Shit"]
            await self.bot.automod.upsert({"_id": str(message.guild.id) + " - Words", "words": words})

        if message.content.startswith(f"<@!{self.bot.user.id}>") and len(message.content) == len(f"<@!{self.bot.user.id}>"):
            data = await self.bot.prefixes.get_by_id(message.guild.id)
            if not data or "prefix" not in data:
                prefix = "-"
            else:
                prefix = data["prefix"]
                
            await message.channel.send(f"My prefix here is `{prefix}`", delete_after=15)

        elif message.content.lower().startswith("hello") or message.content.lower().startswith(
                "hi") or message.content.lower().startswith("hey"):
            embed = discord.Embed(colour=random.choice(self.bot.color_list))
            embed.title = "Hey there!"
            embed.description = f"Nice to see you**!**"
            await message.channel.send(embed=embed)

        elif message.content.lower().startswith("help"):
            await message.channel.send("Hey! Why don't you run the help command with `-help`")

        if message.content.lower().endswith("-hide"):
            await self.bot.process_commands(message)
            await message.delete()
            return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignore these errors
        ignored = commands.UserInputError
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(colour=discord.Color.red())
            embed.description = "<:ImpulseError:776181402382106745> **Command Does Not Exist!**"
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            await ctx.send("Hey! You lack permission to use this command.")

        else:
            raise error

def get_automod(guildid):
    data = json_loader.read_json("automod")

    try:
        if data[guildid]:
            return True

        else:
            return False

    except KeyError:
        data[guildid] = False
        json_loader.write_json(data, 'automod')


def setup(bot):
    bot.add_cog(Events(bot))
