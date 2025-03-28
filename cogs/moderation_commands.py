# Imports
import discord
from discord.ext import commands
import random
from utils import json_loader


# Setup
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot moderation commands are online.\n---------")

    # ----------------------------------------------------------------------

    # COMMANDS

    # Kick
    @commands.command(description="You can kick people with this command.")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        kick_embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        if member == ctx.message.author:
            kick_embed.title = "**Command Error**"
            kick_embed.description = f"**:x: Why this happened:**\nYou cannot kick yourself"
            await ctx.send(embed=kick_embed)
            return

        if reason is None:
            reason = "For being a jerk!"

        message = f"You have been kicked from {ctx.guild.name} for {reason}"
        await member.send(message)
        kick_embed.title = "**Kick Member**"
        kick_embed.description = f"**{member.mention}** has been kicked!\nReason: {reason}"
        kick_embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=kick_embed)
        await member.kick(reason=reason)

    # Ban
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        ban_embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        if member == ctx.message.author:
            ban_embed.title = "**Command Error**"
            ban_embed.description = f"**:x: Why this happened:**\nYou cannot ban yourself"
            await ctx.send(embed=ban_embed)
            return

        if reason is None:
            reason = "For being a jerk!"

        message = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.send(message)
        ban_embed.title = "**Ban Member**"
        ban_embed.description = f"**{member}** has been banned from {ctx.guild.name}!\n**Reason:** {reason}"
        ban_embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=ban_embed)
        await member.ban(reason=reason)

    # Mute
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        mute_embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        if member == ctx.message.author:
            mute_embed.title = "**Command Error**"
            mute_embed.description = f"**:x: Why this happened:**\nYou cannot mute yourself"
            await ctx.send(embed=mute_embed)
            return

        if reason is None:
            reason = "For being a jerk!"

        mute_embed.title = "**Mute Member:**"
        mute_embed.description = f"**{member.mention}** has been muted. The user can no longer chat.\nReason: {reason}"
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        mute_embed.set_thumbnail(url=member.avatar_url)
        await member.add_roles(role)
        await ctx.send(embed=mute_embed)

    # Unmute
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        unmute_embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        unmute_embed.title = "**Mute Member:**"
        unmute_embed.description = f"**{member.mention}** has been unmuted. They has re-gained the ability to chat.\nReason: {reason}"
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        unmute_embed.set_thumbnail(url=member.avatar_url)
        await member.remove_roles(role)
        await ctx.send(embed=unmute_embed)

    # Clear
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Clear**"
        embed.description = f'You have succesfully cleared **{amount}** messages!'
        await ctx.send(embed=embed, delete_after=5)

    # Set Prefix
    @commands.command(name="set_prefix", aliases=["changeprefix", "setprefix"], description="Change your guilds prefix!", usage="[prefix]")
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix):
        await self.bot.on_ready()
        await self.bot.prefixes.upsert({"_id": ctx.guild.id, "prefix": prefix})

        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Set Prefix:**"
        embed.description = f"The guild prefix has been set to `{prefix}`!"
        await ctx.send(embed=embed)

    # Delete Prefix
    @commands.command(name='deleteprefix', aliases=['dp'], description="Delete your guilds prefix!")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def deleteprefix(self, ctx):
        await self.bot.prefixes.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("This guilds prefix has been set back to the default")

    # AutoMod
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def automod(self, ctx):
        automod = await self.bot.automod.find(ctx.guild.id)

        if automod["enabled"] is True:
            await self.bot.automod.upsert({"_id": ctx.guild.id, "enabled": False})
            toggle = "OFF"

        elif automod["enabled"] is False:
            await self.bot.automod.upsert({"_id": ctx.guild.id, "enabled": True})
            toggle = "ON"

        await ctx.send(f"Automod has been toggled {toggle}!")

    # -------------------------------------------------------------------

    # Error Handlers

    # Kick Error
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n1. You did not specify who you wanted to kick. You should have wrote it like this:\n ``-kick [member] [reason(optional)]``"
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n You do not have the permission to use this command."
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\nMember not found."
            await ctx.send(embed=embed)

        else:
            raise error

    # Ban Error
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n1. You did not specify who you wanted to ban. You should have wrote it like this:\n ``-ban [member] [reason(optional)]``"
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n You do not have the permission to use this command."
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\nMember not found."
            await ctx.send(embed=embed)

        else:
            raise error

    # Mute Error
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n1. You did not specify who you wanted to mute. You should have wrote it like this:\n ``-mute [member] [reason(optional)]``"
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n You do not have the permission to use this command."
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\nMember not found."
            await ctx.send(embed=embed)

        else:
            raise error

    # Unmute Error
    @unmute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n1. You did not specify who you wanted to unmute. You should have wrote it like this:\n ``-unmute [member] [reason(optional)]``"
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n You do not have the permission to use this command."
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\nMember not found."
            await ctx.send(embed=embed)

        else:
            raise error

    # Clear Error
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n1. You did not specify the amount of messages you wanted to clear. You should have wrote it like this:\n ``-clear [amount]``"
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n You do not have the permission to use this command."
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 60)

            if int(h) == 0 and int(m) == 0:
                embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
                embed.title = "**Command Cooldown:**"
                embed.description = f"**Why this happened:**\nThis command is on a cooldown of **{int(s)} seconds**!"
                await ctx.send(embed=embed)

            elif int(d) == 0 and int(h) == 0 and int(m) != 0:
                embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
                embed.title = "**Command Cooldown:**"
                embed.description = f"**Why this happened:**\nThis command is on a cooldown of **{int(m)} minutes** and **{int(s)} seconds**!"
                await ctx.send(embed=embed)

            elif int(d) == 0 and int(h) != 0:
                embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
                embed.title = "**Command Cooldown:**"
                embed.description = f"**Why this happened:**\nThis command is on a cooldown of **{int(h)} hours**, **{int(m)} minutes** and **{int(s)} seconds**!"
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
                embed.title = "**Command Cooldown:**"
                embed.description = f"**Why this happened:**\nThis command is on a cooldown of **{int(d)} days**, **{int(h)} hours**, **{int(m)} minutes** and **{int(s)}!"
                await ctx.send(embed=embed)

        else:
            raise error

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n** :x: Why this happened:**\n1. You did not specify the new command prefix. You should have wrote it like this:\n ``-set_prefix [prefix]``"
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)

        else:
            raise error


# Add Cog
def setup(bot):
    bot.add_cog(Moderation(bot))
