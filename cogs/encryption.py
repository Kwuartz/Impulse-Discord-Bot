# Imports
import discord
from discord.ext import commands
import random

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ @'
LETTERS = LETTERS.lower()


# Setup
class Encryption(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot Encryption commands are online.\n---------")

    # Encrypt
    @commands.command()
    async def encrypt(self, ctx, *, string_msg=None):
        if string_msg is None:
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n**:x: Why this happened:**\nYou did not specify what you want to encrypt. You should have wrote it like this:\n ``-encrypt [message]``"
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)

        encrypted = ''
        for chars in string_msg:
            chars = chars.lower()
            if chars in LETTERS:
                num = LETTERS.find(chars)
                num += 1
                encrypted += LETTERS[num]

        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Encryption Result:**"
        embed.description = f"**Original Message** {string_msg}\n**Encrypted Message:** ||{encrypted}||"
        await ctx.send(embed=embed)

    # Encrypt
    @commands.command()
    async def decrypt(self, ctx, *, string_msg):

        if string_msg is None:
            embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
            embed.title = "**COMMAND ERROR:**"
            embed.description = f"\n\n**:x: Why this happened:**\nYou did not specify what you want to decrypt. You should have wrote it like this:\n ``-decrypt [message]``"
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)

        decrypted = ''
        for chars in string_msg:
            if chars in LETTERS:
                num = LETTERS.find(chars)
                num -= 1
                decrypted += LETTERS[num]

        embed = discord.Embed(colour=random.choice(self.bot.color_list), timestamp=ctx.message.created_at)
        embed.title = "**Encryption Result:**"
        embed.description = f"**Original Message** {string_msg}\n**Decrypted Message:** ||{decrypted}||"
        await ctx.send(embed=embed)


# Add Cog
def setup(bot):
    bot.add_cog(Encryption(bot))
