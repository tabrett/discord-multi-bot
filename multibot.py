import os
import re
import time
import json
import random
import logging
import datetime
import asyncio
import aiohttp

from random import ( randint, seed )

# from discord import ( Embed, Client )
import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs import help as help_cog
from cogs import info as info_cog
from cogs import rng as rng_cog
from cogs import channel_move as cmove_cog

from settings.config import Config as config

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%s(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# client = Client(command_prefix)
bot = Bot(description='MultiBot', command_prefix=config.COMMAND_PREFIX)

start_time = datetime.datetime.now()                                            


#=========================
# command listeners
#=========================
@bot.command()
async def prefix():
    bot.say()


@bot.command(aliases=['flip'])
async def coinflip():
    """Returns result of a heads/tails coin flip"""
    await bot.say(rng_cog.coin_flip())


@bot.command(pass_context=True, aliases=['channels'])
async def available_channels(ctx):
    """Lists all channels currently accessible by the bot"""
    valid_channels = bot.get_all_channels()
    channel_list = [ channel.name for channel in valid_channels ]
    msg = ",".join(channel_list)
    await bot.say(msg)


@bot.command(pass_context=True)
async def uptime(ctx):
    await bot.say(info_cog.time_delta(datetime.datetime.now() 
                                     -start_time))

@bot.command(pass_context=True)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await bot.send_typing(channel)
    t2 = time.perf_counter()
    await bot.say('Pong! It took {}ms.'.format(round((t2-t1))))


@bot.command(pass_context=True)
async def roll(ctx):

    dice_val, dice_count = rng_cog.roll_parse(ctx.message.content)
    hit_cap = False
    
    # hard cap rolls at rollCap value
    try: 
        if int(dice_count) > config.ROLL_CAP:
            dice_count = config.ROLL_CAP
            hit_cap = True
    except:
        dice_count = 0

    # returns help text first
    if dice_val.lower() in config.BOT_COMMANDS:
        if (dice_val.lower() == 'commands' or
            dice_val.lower() == 'help'):
            help_table = help_cog.build_help_message()

            await bot.say(help_table) # embed=get_HelpImbed(help_table))
        elif dice_val.lower() == 'info':
            await bot.say(embed=info_cog.build_info_message())

    elif int(dice_val) in config.VALID_DICE:
        await bot.say(embed=rng_cog.build_RollResult(ctx.message.author.name, 
                                                     int(dice_val), 
                                                     int(dice_count), 
                                                     hit_cap))
    else:
        msg = 'You fucked up. Pick a valid die or command.'
        await bot.say(msg)
        await bot.say(embed=help_cog.get_help_imbed(help_table))


@bot.command(pass_context=True, aliases=['grantbot'])
async def grant_bot(ctx):
    # message.content.startswith(': fire')):
    msg = ': fire'
    time.sleep(config.BOT_RESPONSE_DELAY)
    await bot.add_reaction(ctx.message, u'\U0001F525')
    await bot.say(msg)
    

@bot.command(pass_context=True, aliases=['michaelbot'])
async def michael_bot(ctx):
    # message.content.startswith(':0')):
    msg = ':0'
    time.sleep(config.BOT_RESPONSE_DELAY)
    await bot.add_reaction(ctx.message, u'\U00002615')
    await bot.say(msg)


@bot.command(pass_context=True, aliases=['telorbot','taytaybot'])
async def taylor_bot(ctx):
    msg = 'No u'
    time.sleep(config.BOT_RESPONSE_DELAY)
    await bot.say(msg)


@bot.command(pass_context=True, aliases=['chibot','chihuahuabot'])
async def chihuahua_bot(ctx):
    time.sleep(config.BOT_RESPONSE_DELAY)
    # embed.set_image(url="https://imgur.com/a/tiW7M9A")
    await bot.send_file(ctx.message.channel, "assets/im-sorry.png")


@bot.command(pass_context=True)
async def raid(ctx):
    landing_channel = discord.utils.get(ctx.message.server.channels,
                                        name=config.LANDING_CHANNEL_NAME,
                                        type=discord.ChannelType.voice)

    target_channel = discord.utils.get(ctx.message.server.channels,
                                       name=config.TARGET_CHANNEL_NAME,
                                       type=discord.ChannelType.voice)
    
    for member in landing_channel.voice_members:
        await bot.say(member)
        await bot.move_member(member, target_channel)
    
    await bot.say('Users moved.')


@bot.command(pass_context=True, aliases=['config', 'botconfig'])
async def bot_config(ctx, *args):
    await bot.say(args)

    config_list = [ (k, config.__dict__[k]) for k in config.__dict__
                            if not k.startswith('_')]
    
    for item in config_list:
        await bot.say(item)

    # msg = '\n'.join(config_list)
    # await bot.say(msg)

    # for k in config.__dict__:
    #     if not k.startswith('_'):
    #         # msg
    #         try:
    #             msg = '\n'.join('%s : %s' %(k, config.__dict__[k]))
    #             await bot.say(msg)
    #             # await bot.say('%s : %s\n' % (k, config.__dict__[k]))
    #         # except AttributeError:
    #             # await bot.say('%s : %s\n' % (k, config.__dict__[k].encode("utf-8")))
    #         except:
    #             pass

# async def config(ctx, *args):
    # if args is None:
    #     pass
    # return

#=========================
# non-command listeners
#=========================
@bot.event
async def on_message(message):
    await bot.process_commands(message)                                         # allow commands to be processed first

    if message.author == bot.user:
        return 

    if message.mention_everyone:
        time.sleep(config.BOT_RESPONSE_DELAY)
        await bot.add_reaction(message, u'\U0001F621')
        await bot.send_message(message.channel, 
                              (random.choice(config.AT_EVERYONE_RESPONSES) 
                                          % (message.author.id)))

@bot.event
async def on_ready():
    print('Logged in as ', bot.user.name, bot.user.id, bot.user.bot)


#=========================
# run bot
#=========================
bot.run(config._BOT_KEY)