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
        if re.match('^\d{1,2}[dD]\d{1,3}$', dice):
            # dice_types = [2, 4, 6, 8, 10, 12, 20, 100]
            arg = dice.split('d')
            num_dice = int(arg[0])
            dice_type = int(arg[1])
            rolls = []
            # if dice_type not in dice_types:
            #     await ctx.send(f'Please specify a valid dice type')
            #     return False
            for i in range(0, num_dice):
                rolls.append(random.randint(1, dice_type))
            await ctx.send(f'Rolling {dice} \nResults: {", ".join(str(x) for x in rolls)}')
        else:
            await ctx.send('Please specify a valid dice type')
def setup(bot):
    bot.add_cog(Dice_Commands(bot))
