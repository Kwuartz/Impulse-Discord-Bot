# Imports
import discord
from discord.ext import commands
import random
from pathlib import Path

from utils import json_loader

# Current Working Directory
cwd = Path(__file__).parents[1]
cwd = str(cwd)

# Secret
secret_file = json_loader.read_json("secrets")


# Setup
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot basic commands are online.\n---------")
        self.bot.version = "1.4.3"
        self.bot.date = "4th October 2020"

    # Greeting
    @commands.command(aliases=["hello", "hey"], description="Greets you.")
    async def hi(self, ctx):
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "Hey there!"
        embed.description = f"Nice to see you **{ctx.author.mention}!**"
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, *cog): # Change Name If You Want Dreigon Stupid
        data = await self.bot.prefixes.get_by_id(ctx.message.guild.id)
        if not data or "prefix" not in data:
            prefix = "."
        else:
            prefix = data["prefix"]

        if cog: # If Cogs Are Specified
            cogs = len(cog)

            if cogs > 1: # If too many categories
                help = discord.Embed(color=123456)
                help.title = 'Error'
                help.description = 'Only 1 category allowed'

            elif cogs == 1:
                Exists = False # Default

                for a in self.bot.cogs:
                    for b in cog:
                        if a == b:
                            help = discord.Embed(color=123456)
                            help.title= 'Commands'
                            help.description = self.bot.cogs[cog[0]].__doc__

                            for command in self.bot.get_cog(a).get_commands():
                                if not command.hidden:
                                    help.add_field(name=f"{prefix}{command.name}", value=command.help, inline=False)
                            Exists = True

                if Exists == False:
                    help = discord.Embed(color=123456)
                    help.title = 'Error'
                    help.description = 'That category doesnt exist'

                await ctx.message.author.send(embed=help)

        else:  # If No Cogs Are Specified
            help = discord.Embed(color=123456)
            help.title = 'Help Categories!'
            help.description = 'Use Help [Category] To Find Out More'
            categories_description = ''

            for CogNumber in self.bot.cogs:
                if CogNumber is not "Help":
                    categories_description += (f'{CogNumber}' + '\n')  # Add Cog Number And Name

            help.add_field(inline=False, name='Category',
                           value=categories_description[0:len(categories_description) - 1])  # Add Field For Cogs

            await ctx.message.author.send(embed=help)



    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.add_field(name="Owner", value=ctx.guild.owner)
        embed.add_field(name="ID", value=ctx.guild.id)
        embed.add_field(name="Region", value=ctx.guild.region)
        embed.add_field(name="Categories", value=str(len(ctx.guild.categories)))
        embed.add_field(name="Text Channels", value=str(len(ctx.guild.text_channels)))
        embed.add_field(name="Voice Channels", value=str(len(ctx.guild.voice_channels)))
        embed.add_field(name="Members", value=str(ctx.guild.member_count))
        embed.add_field(name="Roles", value=str(len(ctx.guild.roles)))
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        user = user or ctx.author

        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.set_author(name=f"{user.name} - Avatar", icon_url=user.avatar_url)
        embed.set_image(url=user.avatar_url_as(size=1024))
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def joinedat(self, ctx, *, user: discord.Member = None):
        """ Check when a user joined the current server """
        user = user or ctx.author

        embed = discord.Embed(colour=user.top_role.colour.value)
        embed.set_thumbnail(url=user.avatar_url)
        embed.description = f'**{user}** joined **{ctx.guild.name}**\n{user.joined_at}'
        await ctx.send(embed=embed)

    # ChannelStats
    @commands.command(aliases=['cs'])
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channelstats(self, ctx):
        """
        Sends a nice fancy embed with some channel stats
        !channelstats
        """
        channel = ctx.channel
        embed = discord.Embed(title=f"Stats for **{channel.name}**",
                              description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",
                              color=random.choice(self.bot.color_list))
        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel Id", value=channel.id, inline=False)
        embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
        embed.add_field(name="Channel Position", value=channel.position, inline=False)
        embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
        embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
        embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
        embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
        embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
        embed.add_field(name="Channel Hash", value=str(hash(channel)), inline=False)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    # Ping
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Pong!**"
        embed.description = f"Your latency is {round(self.bot.latency * 1000)}ms"
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    # UserInfo
    @commands.command(aliases=["whois"])
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author

        status = str(member.status).capitalize()

        roles = [role for role in member.roles]
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)

        embed.set_author(name="Bot Stats", icon_url=member.avatar_url)

        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"ID: {member.id}", icon_url=member.avatar_url)

        embed.add_field(name="``Display Name:``", value=f"{member.mention}")

        embed.add_field(name="``Created Account On:``", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="``Joined Server On:``", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="``Roles:``", value="".join([role.mention + "\n" for role in roles]))
        embed.add_field(name="``Highest Role:``", value=member.top_role.mention)

        embed.add_field(name="``Status:``", value=status)

        await ctx.send(embed=embed)

    # Colour Gen
    @commands.command()
    async def colourgen(self, ctx):
        clr = random.randint(0, 99999)
        clr_embed = discord.Embed(colour=clr)
        clr_embed.title = "Your colour is on this embed!"
        clr_embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=clr_embed)

    # Echo
    @commands.command()
    async def echo(self, ctx, *, content: str):
        await ctx.channel.purge(limit=1)
        await ctx.send(content)

    # RandomNumGen
    @commands.command()
    async def randomnum(self, ctx, startnumber: int, endnumber: int):
        if startnumber > endnumber:
            start_number = startnumber
            startnumber = endnumber
            endnumber = start_number

        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Random Number Generator**"
        randomnum = random.randint(startnumber, endnumber)
        embed.description = f"**Starting Number:** {startnumber}\n**Ending Number:** {endnumber}\n **Random Number:** ||{randomnum}||"
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    # Coinflip
    @commands.command()
    async def coinflip(self, ctx, player1choice, player2choice):
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Coinflip:**"
        randomnumgenerator = random.randint(1, 2)

        if randomnumgenerator == 1:
            result = "heads"
        else:
            result = "tails"

        if result == player1choice:
            winner = "Player 1"

        elif result == player2choice:
            winner = "Player 2"

        else:
            winner = "Error"

        embed.description = f"**The coin landed on** ||{result}|| \n**The winner is ||{winner}||**"
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    # ------------------------------------------------------------------

    # Error Handler

    # Echo
    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n**:x: Why this happened:**\n1. You did not specify what you wanted to repaet with the echo command. You should have wrote it like this:\n ``-echo [text]``"
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        else:
            raise error

    # RandomNumGen
    @randomnum.error
    async def randomnum_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n**:x: Why this happened:**\n1. You did not specify the starting and ending number. You should have wrote it like this:\n ``-randomnum [num1] [num2]``"
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        else:
            raise error

    # Coinflip
    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print("yes")
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n**:x: Why this happened:**\n1. You did not specify the choice of PLayer 1 and Player 2. You should have wrote it like this:\n ``-coinflip [player1choice] [player2choice]``"
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        else:
            raise error


# Add Cog
def setup(bot):
    bot.add_cog(General(bot))
