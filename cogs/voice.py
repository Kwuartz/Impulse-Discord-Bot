import discord
from discord.ext import commands
import youtube_dl


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()


# Add Cog
def setup(bot):
    bot.add_cog(Voice(bot))
