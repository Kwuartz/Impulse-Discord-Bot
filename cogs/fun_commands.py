#Imports
import discord
from discord.ext import commands
import random
from pathlib import Path
import secrets

from utils import lists, json_loader

#Variables
cwd = Path(__file__).parents[1]
cwd = str(cwd)

owner_id = 567327597642383420

randint = random.randint

#Secrets
secret_file = json_loader.read_json("secrets")


#Setup
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot fun commands are online.\n---------")

    #Animal
    @commands.command()
    async def animal(self, ctx):
        animal_chosen = random.choice(lists.animal_selection)
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Animal!**"
        embed.description = "**Here you go:**"
        embed.set_image(url=animal_chosen)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    #Ebola Test
    @commands.command()
    async def ebolatest(self, ctx):
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Test Results:**"
        embed.description = f"**Whoa!** Your chance of getting ebola is **||{randint(1, 100)}%||**"
        embed.set_image(url='https://i.imgur.com/JocMAl0.jpg')
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    #Faker
    @commands.command()
    async def faker(self, ctx):
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Are you???**"
        embed.description = f"Are you faker irl or what?\n\n"
        embed.set_image(url = 'https://gamepedia.cursecdn.com/lolesports_gamepedia_en/4/41/SKT_Faker_2018_Split_2.png')
        embed.set_footer(text = f"League of Legends Reference.")
        await ctx.send(embed = embed)

    #Spam Ping
    @commands.command(aliases = ["spam"])
    @commands.cooldown(1, 90, commands.BucketType.user)
    async def spamping(self, ctx, victim : discord.Member, amount):

        #Converting
        Amount = int(amount)
        if ctx.author.id == owner_id:
            print("Owner had bypassed spam ping limit!\n---------")

        elif Amount > 10 and ctx.author.id != owner_id:
            await ctx.send(f"Sorry you cannot ping your victim more than 10 times unless you are the owner - KWuartz!")

        x = 0
        while x < Amount:
            async with ctx.typing():
                await ctx.send(f"Sorry {victim.mention}, I am forced to do this!")
                x = x + 1


        for i in amount:
            async with ctx.typing():
                await ctx.send(f"Sorry {victim.mention}, I am forced to do this!")

    #Cool
    @commands.command()
    async def cool(self, ctx):
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Is Impulse cool?**"
        embed.description = f'Yes, the bot is\n**COOL**.'
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password for you """
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    #Penguin
    @commands.command()
    async def penguin(self, ctx):
        penguin_chosen = random.choice(lists.penguin_selection)
        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Penguin!**"
        embed.description = "**Here you go:**"
        embed.set_image(url=penguin_chosen)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    #8Ball
    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """

        answer = random.choice(lists.ballresponses)

        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**🎱 8Ball Result:**"
        embed.description = f"**Question:** {question}\n**Answer:** ||{answer}||"
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    #-------------------------------------------------------------------------------

    #Error Handlers

    #8ball
    @eightball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n**:x: Why this happened:**\n1. You did not specify the question you wanted to answer with the 8ball command. You should have wrote it like this:\n ``-8ball [Question]``"
            await ctx.send(embed = embed)

        else:
            raise error

    #Spam Ping
    @spamping.error
    async def spamping_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n**:x: Why this happened:**\nYou did not specify who your victim is 2. You did not specify how many times you wanted to spam ping your victim. You should have wrote it like this:\n ``-spamping [victim] [amount]``"
            await ctx.send(embed = embed)
            ctx.command.reset_cooldown(ctx)


#Add Cog
def setup(bot):
   bot.add_cog(Fun(bot))
