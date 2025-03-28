# Imports
import random
from os import path
from pathlib import Path

import discord
from discord.ext import commands

cwd = Path(__file__).parents[1]
cwd = str(cwd)


# Setup
class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot owner commands are online.\n---------")

    # Logout
    @commands.command(aliases=["shutdown", "off"])
    @commands.is_owner()
    async def logout(self, ctx):
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Bot Shutdown:**"
        embed.description = f"Yes **{ctx.author.mention}**\n I am now shutting down..."
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        await self.bot.logout

    # Load
    @commands.command(aliases=["cogload"])
    @commands.is_owner()
    async def load(self, ctx, extension):

        if extension.endswith(".py"):
            extension = extension[:-3]
            print("Extension Unloaded\n---------")

            if extension.endswith('_commands'):
                return

            else:
                extension = extension + "_commands"

        elif extension.endswith('_commands'):
            print("Extension Unloaded\n---------")

        else:
            extension = extension + "_commands"

        if path.exists("cogs.{extension}") is False:
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**Command Load Error:**"
            embed.description = f"Sorry **{ctx.author.mention}** but this file does not exist!"
            embed.set_thumbnail(url=ctx.author.avatar_url)

        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Cog Load:**"
        embed.description = f"Yes **{ctx.author.mention}!**\n**Loading {extension}...**"
        embed.set_thumbnail(url=ctx.author.avatar_url)
        self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(embed=embed)

    # Unload
    @commands.command(aliases=["cogunload"])
    @commands.is_owner()
    async def unload(self, ctx, extension):
        if extension.endswith(".py"):
            extension = extension[:-3]
            print("Extension Unloaded\n---------")

            if extension.endswith('_commands'):
                return

            else:
                extension = extension + "_commands"

        elif extension.endswith('_commands'):
            print("Extension Unloaded\n---------")

        else:
            extension = extension + "_commands"

        if path.exists("cogs.{extension}") is False:
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**Command Unload Error:**"
            embed.description = f"Sorry **{ctx.author.mention}** but this file does not exist!"
            embed.set_thumbnail(url=ctx.author.avatar_url)

        if extension == "owner_commands":
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**Command Load Error:**"
            embed.description = f"Sorry **{ctx.author.mention}** but you cannot unload owner_commands because it is from here that you load commands!"
            embed.set_footer(text="Sorry for any inconviences.")
            embed.set_thumbnail(url=ctx.author.avatar_url)

        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Cog Unload:**"
        embed.description = f"Yes **{ctx.author.mention}!**\n**Unloading: {extension}...**"
        embed.set_thumbnail(url=ctx.author.avatar_url)
        self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(embed=embed)

    # Blacklist
    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("Hey, you cannot blacklist yourself!")
            return

        try:
            await self.bot.blacklist.upsert({"name": user.name, "_id": user.id})

        except:
            await ctx.send("This user is already blacklisted!", delete_after=5)

        self.bot.blacklisted_users.append(user.id)

        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Blacklist:**"
        embed.description = f"Hey, I have blacklisted {user.mention} for you."
        await ctx.send(embed=embed)

    # Unblacklist
    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        try:
            self.bot.blacklisted_users.remove(user.id)

        except ValueError:
            await ctx.send("This user is not blacklisted!", delete_after=5)
            return

        await self.bot.blacklist.delete(user.id)

        await ctx.send("This user is not blacklisted!", delete_after=5)

        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Unlacklist:**"
        embed.description = f"Hey, I have unblacklisted {user.mention} for you."
        await ctx.send(embed=embed)

    # ---------------------------------------------------------------------------

    # Error Handlers
    @logout.error
    async def logout_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n You are not my owner {ctx.author.mention}!"
            await ctx.send(embed=embed)

        else:
            raise error

    @load.error
    async def load_error(self, ctx, error):

        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n You are not my owner {ctx.author.mention}!"
            await ctx.send(embed=embed)

        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n Extension already loaded!"
            await ctx.send(embed=embed)

        else:
            raise error

    @unload.error
    async def unload_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n You are not my owner {ctx.author.mention}!"
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n Choose an extension!"
            await ctx.send(embed=embed)

        elif isinstance(error, commands.ExtensionNotFound):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n Extension not found!"
            await ctx.send(embed=embed)

        else:
            raise error


# Add Cog
def setup(bot):
    bot.add_cog(Owner(bot))
