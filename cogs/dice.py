import discord
from discord.ext import commands
import re
import random

class Dice_Commands(commands.Cog, name='Dice Commands'):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command.cog = self
    @commands.command(help=f"Roll some dice")
    async def roll(self, ctx, dice):
        arg = re.search('^(\d{1,2})[dD](\d{1,3})$', dice)
        if arg:
            arg = re.split('d', dice, flags=re.IGNORECASE)
            num_dice = int(arg[0])
            dice_type = int(arg[1])
            rolls = []
            for i in range(0, num_dice):
                rolls.append(random.randint(1, dice_type))
            roll_sum = sum(rolls)
            await ctx.send(f'Rolling {dice} \nResults: {", ".join(str(x) for x in rolls)}\n{("Sum: " + str(roll_sum)) if num_dice > 1 else ""}')
        else:
            await ctx.send('Please specify a valid dice type')
def setup(bot):
    bot.add_cog(Dice_Commands(bot))
