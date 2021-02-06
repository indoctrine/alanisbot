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

async def load_dependencies():
    async with aiofiles.open('ironic.json', 'r') as f:
        ironic_contents = await f.read()
    async with aiofiles.open('hack_command.json', 'r') as g:
        hack_contents = await g.read()
    async with aiofiles.open('auth.json', 'r') as h:
        creds = await h.read()
    return json.loads(ironic_contents), json.loads(hack_contents), json.loads(creds)

intents = discord.Intents.default()
intents.members = True # Intent allows us to get users that haven't been seen yet
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
bot.ironic_statements = []
bot.ironic_statements, bot.hack_data, bot.creds = asyncio.get_event_loop().run_until_complete(load_dependencies())
extensions = ['cogs.hack']

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Ironic - Alanis Morissette', url='https://open.spotify.com/track/29YBihzQOmat0U74k4ukdx?si=RNDU7bMzSMKRzGYwnyqA-g'))
    logging.info(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    ironic_regex = re.compile(r'[i|l1]\s*r\s*[o0]\s*n\s*[yi|l1]', re.IGNORECASE)
    ctx = message.channel
    if message.author.id is bot.user.id:
        return
    if ':<' in message.content:
        bot.hack_data['attempts'] += 1
        randompercentage = math.floor(100 * math.pow((random.random()), (bot.hack_data['difficulty']/bot.hack_data['attempts'])))
        if(randompercentage == 100):
            bot.hack_data['triggers'] += 1
            await ctx.send(f"Attempt 0x{bot.hack_data['attempts']} successful. Hacking {randompercentage}% complete. Consequences will never be the same, <@!64909909052887040> has backtraced your IP and the cyberpolice are on their way.");
            bot.hack_data['attempts'] = 0
        else:
            if randompercentage > 60:
                await ctx.send(f'<@!64909909052887040> is getting closer... Hacking {randompercentage}% complete.');
            else:
                await ctx.send(f'<@!64909909052887040> is a big nerd. Hacking in progress, {randompercentage}% complete.')
        async with aiofiles.open('hack_command.json', 'w') as f:
            string_json = json.dumps(bot.hack_data)
            await f.write(string_json)
    elif ironic_regex.search(message.content):
        await ctx.send(random.choice(bot.ironic_statements))
    elif re.search('thot', message.content, flags=re.IGNORECASE):
        await message.add_reaction('🙏')
        await ctx.send(f'Sending thots and prayers to <@!{message.author.id}>')
    await bot.process_commands(message)

try:
    bot.run(bot.creds['token'])
except Exception as e:
    logging.exception(f'Could not connect to Discord {e}')
    sys.exit(1)
