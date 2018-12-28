import os
import re
import time
import json
import random
import logging
import datetime

from random import ( randint, seed )

from discord import ( Embed, Client )
import asyncio
import aiohttp

from cogs import help as help_cog
from cogs import info as info_cog
from cogs import rolls as roll_cog
from cogs import channel_move as cmove_cog

from settings import config

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%s(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# logging.basicConfig(level=logging.DEBUG)

# discord_key = os.environ.get('DISCORD_SECRET')
discord_key = config.bot_key

client = Client()

start_time = datetime.datetime.now()                                            



#=========================
# listeners
#=========================
@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content.startswith('!channels'):
        valid_channels = client.get_all_channels()
        channel_list = [channel.name for channel in valid_channels]
        msg = ",".join(channel_list)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!roll'):
        diceVal, diceCount = roll_cog.roll_parse(message.content)
        hitCap = False
        
        # hard cap rolls at rollCap value
        try: 
            if int(diceCount) > config.roll_cap:
                diceCount = config.roll_cap
                hitCap = True
        except:
            diceCount = 0

        # returns help text first
        if diceVal.lower() in config.bot_commands:
            if (diceVal.lower() == 'commands' or
                diceVal.lower() == 'help'):
                help_table = help_cog.build_HelpMessage()

                await client.send_message(message.channel, help_table) # embed=get_HelpImbed(help_table))
            elif diceVal.lower() == 'info':
                await client.send_message(message.channel, 
                                            embed=info_cog.build_InfoMessage())
        elif int(diceVal) in config.valid_dice:
            await client.send_message(message.channel, 
                                        embed=roll_cog.build_RollResult(
                                                    message.author.name, 
                                                    int(diceVal), 
                                                    int(diceCount), 
                                                    hitCap
                                                ))
        else:
            msg = 'You fucked up. Pick a valid die or command.'
            await client.send_message(message.channel, msg)
            await client.send_message(message.channel, 
                                        embed=help_cog.get_HelpImbed(help_table))

    elif (message.content.startswith('!grantbot') or
            message.content.startswith(': fire')):
        msg = ': fire'
        time.sleep(1)
        await client.add_reaction(message, u'\U0001F525')
        await client.send_message(message.channel, msg)

    elif (message.content.startswith('!michaelbot') or 
            message.content.startswith(':0')):
        msg = ':0'
        time.sleep(1)
        await client.add_reaction(message, u'\U00002615')        
        await client.send_message(message.channel, msg)

    elif (message.content.startswith('!telorbot') or 
            message.content.startswith('!taytaybot')):
        msg = 'No u'
        time.sleep(1)
        # await client.add_reaction(message, u'\U0000XXXX')
        await client.send_message(message.channel, msg)    

    elif (message.content.startswith('!chibot') or 
            message.content.startswith('!chihuahuabot')):
        time.sleep(1)
        # embed = Embed()
        # embed.set_image(url="https://imgur.com/a/tiW7M9A")
        # await client.send_message(message.channel, embed=embed)
        await client.send_file(message.channel, "assets/im-sorry.png")

    elif (message.content.startswith('!uptime')):
        await client.send_message(message.channel, 
                                    info_cog.time_delta(datetime.datetime.now() 
                                                       -start_time))
                                                       
    if message.mention_everyone:
        time.sleep(1)
        await client.add_reaction(message, u'\U0001F621')
        await client.send_message(message.channel, 
                                    (random.choice(config.at_everyone_responses) 
                                                    % (message.author.id)))

@client.event
async def on_ready():
    print('Logged in as ', client.user.name, client.user.id, '--------')


#=========================
# run bot
#=========================
client.run(discord_key)