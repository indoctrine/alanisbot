import discord
from discord.ext import commands
import logging
import json
import sys
import random
import aiofiles
import asyncio
import math
import re

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', stream=sys.stderr,level=logging.INFO)

ironic_statements = []
global hack_data

async def load_dependencies():
    async with aiofiles.open('ironic.json', 'r') as f:
        ironic_contents = await f.read()
    async with aiofiles.open('hack_command.json', 'r') as g:
        hack_contents = await g.read()
    async with aiofiles.open('auth.json', 'r') as h:
        creds = await h.read()
    return json.loads(ironic_contents), json.loads(hack_contents), json.loads(creds)
ironic_statements, hack_data, creds = asyncio.get_event_loop().run_until_complete(load_dependencies())

intents = discord.Intents.default()
intents.members = True # Intent allows us to get users that haven't been seen yet
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Ironic - Alanis Morissette', url='https://open.spotify.com/track/29YBihzQOmat0U74k4ukdx?si=RNDU7bMzSMKRzGYwnyqA-g'))
    logging.info(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    global hack_data
    ironic_regex = re.compile(r'[i|l1]\s*r\s*[o0]\s*n\s*[yi|l1]', re.IGNORECASE)
    ctx = message.channel
    if message.author.id is bot.user.id:
        return
    if ':<' in message.content:
        hack_data['attempts'] += 1
        randompercentage = math.floor(100 * math.pow((random.random()), (hack_data['difficulty']/hack_data['attempts'])))
        if(randompercentage == 100):
            hack_data['triggers'] += 1
            await ctx.send(f"Attempt 0x{hack_data['attempts']} successful. Hacking {randompercentage}% complete. Consequences will never be the same, <@!64909909052887040> has backtraced your IP and the cyberpolice are on their way.");
            hack_data['attempts'] = 0
        else:
            if randompercentage > 60:
                await ctx.send(f'<@!64909909052887040> is getting closer... Hacking {randompercentage}% complete.');
            else:
                await ctx.send(f'<@!64909909052887040> is a big nerd. Hacking in progress, {randompercentage}% complete.')
        async with aiofiles.open('hack_command.json', 'w') as f:
            string_json = json.dumps(hack_data)
            await f.write(string_json)
    elif ironic_regex.search(message.content):
        await ctx.send(random.choice(ironic_statements))
    elif re.search('thot', message.content, flags=re.IGNORECASE):
        await message.add_reaction('🙏')
        await ctx.send(f'Sending thots and prayers to <@!{message.author.id}>')
    await bot.process_commands(message)

class Hack_Commands(commands.Cog, name='Hack Commands'):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command.cog = self
    @commands.command(help=f"{bot.get_user(64909909052887040)} is a Chinese Hackerman who has backtraced your IP {hack_data['triggers']} times")
    async def hax(self, ctx):
        await ctx.send(f"Look out, <@!64909909052887040> has hacked the Gibson {hack_data['triggers']} times!")

bot.add_cog(Hack_Commands(bot))

try:
    bot.run(creds['token'])
except Exception as e:
    logging.exception(f'Could not connect to Discord {e}')
    sys.exit(1)
