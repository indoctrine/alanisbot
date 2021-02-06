import discord
from discord.ext import commands

class Hack_Commands(commands.Cog, name='Hack Commands'):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command.cog = self
    @commands.command(help=f"Zerahl is a Chinese Hackerman who has backtraced your IP")
    async def hax(self, ctx):
        await ctx.send(f"Look out, <@!64909909052887040> has hacked the Gibson {ctx.bot.hack_data['triggers']} times!")
def setup(bot):
    bot.add_cog(Hack_Commands(bot))
