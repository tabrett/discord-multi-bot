import os
import re
import time
import json
import random
import logging
import datetime
import asyncio
import aiohttp

from pprint import pformat
from random import ( randint, seed )

# import discord
from discord import ( Embed, Client, ChannelType )
from discord import utils as disc_utils

from discord.ext import commands
from discord.ext.commands import Bot

from cogs import channel_move as cmove_cog

from cogs.config import Config as config

from cogs.meta import time_delta, build_info_message
from cogs.help import build_help_message, get_help_imbed
from cogs.wiki import ( get_wiki_page, build_wiki_embed, 
                         get_raw_page, build_from_raw )

from cogs.coinflip import coin_flip
from cogs.dice_roll import build_roll_result


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
@bot.command(aliases=['flip'])
async def coinflip():
    """Returns result of a heads/tails coin flip"""
    await bot.say(coin_flip())


@bot.command(pass_context=True, aliases=['channels'])
async def available_channels(ctx):
    """Lists all channels currently accessible by the bot"""
    valid_channels = bot.get_all_channels()
    channel_list = [ channel.name for channel in valid_channels ]
    msg = ",".join(channel_list)
    await bot.say(msg)


@bot.command(pass_context=True)
async def uptime(ctx):
    """Returns the uptime of the bot."""
    await bot.say(time_delta(datetime.datetime.now() 
                                     -start_time))

@bot.command(pass_context=True)
async def ping(ctx):
    """Pings the bot and returns the response time."""

    channel = ctx.message.channel
    t1 = time.perf_counter()
    await bot.send_typing(channel)
    t2 = time.perf_counter()
    await bot.say('Pong! It took {}ms.'.format(round((t2-t1))))


@bot.command(pass_context=True)
async def roll(ctx, *args):
    """Returns the result of a dice roll.
    Ex: !roll 2d20 - Returns result of rolling 2 d20.

    Roll split defaults to 'd', but can be changed in configuration.

    Maximum of 15 dice per roll.  This can be changed in configuration."""

    roll = ctx.message.content.split(' ')[1]
    dice_count, dice_val = map(str, roll.split(config.ROLL_SPLIT))
    hit_cap = False
    
    # hard cap rolls at rollCap value
    try: 
        if int(dice_count) > config.ROLL_CAP:
            dice_count = config.ROLL_CAP
            hit_cap = True
    except:
        dice_count = 0

    if int(dice_val) in config.VALID_DICE:
        await bot.say( '<@%s>' % ctx.message.author.id )
        await bot.say(embed=build_roll_result( ctx.message.author.name, 
                                                int(dice_val), 
                                                int(dice_count), 
                                                hit_cap ) )
    else:
        msg = 'That was not a valid die. Pick a valid die or command.'
        await bot.say(msg)


@bot.command(pass_context=True, aliases=['grantbot'])
async def grant_bot(ctx):
    """Low-effort "meme."
    
    Responds *just* like Grant."""
    msg = ': fire'
    time.sleep(config.BOT_RESPONSE_DELAY)
    await bot.add_reaction(ctx.message, u'\U0001F525')
    await bot.say(msg)
    

@bot.command(pass_context=True, aliases=['michaelbot'])
async def michael_bot(ctx):
    """Low-effort "meme."
    
    Responds *just* like Michael."""
    # message.content.startswith(':0')):
    msg = ':0'
    time.sleep(config.BOT_RESPONSE_DELAY)
    await bot.add_reaction(ctx.message, u'\U00002615')
    await bot.say(msg)


@bot.command(pass_context=True, aliases=['telorbot','taytaybot'])
async def taylor_bot(ctx):
    """Low-effort "meme."
    
    Responds *just* like Tay."""
    msg = 'No u'
    time.sleep(config.BOT_RESPONSE_DELAY)
    await bot.say(msg)


@bot.command(pass_context=True, aliases=['chibot','chihuahuabot'])
async def chihuahua_bot(ctx):
    """Low-effort meme image."""
    time.sleep(config.BOT_RESPONSE_DELAY)
    # embed.set_image(url="https://imgur.com/a/tiW7M9A")
    await bot.send_file(ctx.message.channel, "assets/im-sorry.png")


@bot.command(pass_context=True)
async def raid(ctx):
    """Moves all users from one voice channel to another.

    Channels are designated in the bot configuration, 

    LANDING_CHANNEL_NAME: The starting channel.
    TARGET_CHANNEL_NAME: The channel to move users to.
    """

    landing_channel = disc_utils.get(ctx.message.server.channels,
                                     name=config.LANDING_CHANNEL_NAME,
                                     type=ChannelType.voice)

    target_channel = disc_utils.get(ctx.message.server.channels,
                                    name=config.TARGET_CHANNEL_NAME,
                                    type=ChannelType.voice)
    
    i = 0
    for member in landing_channel.voice_members:
        try:
            await bot.move_member(member, target_channel)
            i+=1
        except:
            await bot.say('%s was not moved.' % member.name)
    
    await bot.say('%s users moved.' % i)


@bot.command(pass_context=True, aliases=['wikibot'])
async def wiki(ctx, *, arg):
    """Queries the Wikipedia API and returns a summary of the page passed as
    an argument.

    Returns similar pages if none found."""
    
    try:
        wiki_embed = build_wiki_embed(get_wiki_page(arg))
        await bot.say(embed=wiki_embed)
    except:
        raw_page = get_raw_page(arg).json()

        if raw_page['type'] != "disambiguation":
            wiki_embed = build_from_raw(raw_page)
            await bot.say(embed=wiki_embed)
        else: 
            await bot.say(embed=Embed(name="Error",
                                        value="Wiki result could not be found.",
                                        inline=True))
    


@bot.command(pass_context=True, aliases=['config', 'botconfig'])
async def bot_config(ctx, *args):
    """Lists the current configuration values for the bot."""
    config_items = { k:v for (k,v) in config.__dict__.items()
                        if not k.startswith('_') }

    config_str = ""
    for item in config_items:
        if isinstance(config_items[item], list):
            list_str = pformat(config_items[item])
            config_str +=("%s: \n %s\n\n" % (item, list_str))
        else:
            config_str += ("%s: %s\n\n" % (item, config_items[item]))

    embed_config = Embed(title="Current Configuration")
    embed_config.add_field(name=u"\u200b", value=config_str, inline=False)

    # TODO: change to private message
    await bot.say(embed=embed_config)


@bot.command(pass_context=True)
async def prefix(ctx):
    """Shows the current command prefix configuration.
    Change the prefix with '!prefix set <new_prefix>'."""
    if 'set' in ctx.message.content:
        if ctx.message.author.server_permissions.administrator:
            msg_content = ctx.message.content.split(" ")
            
            bot.command_prefix = msg_content[2]
            config.COMMAND_PREFIX = msg_content[2]

            logger.info("Bot command prefix set to: '%s'" % config.COMMAND_PREFIX)
            await bot.say("Bot command prefix set to: '%s'" % config.COMMAND_PREFIX)
        else: 
            await bot.say("You don't have permission to do this.")
    else:
        await bot.say("Current bot command prefix: '%s'" % config.COMMAND_PREFIX)


# TODO: Code to change dice roll splitter
# TODO: Code to change Roll Cap
# TODO: Code to add/modify valid dice list
# TODO: Code to add/modify AT_EVERYONE_RESPONSES
# TODO: Code to modify LANDING_CHANNEL_NAME/TARGET_CHANNEL_NAME
# TODO: Code to modify BOT_RESPONSE_DELAY


@bot.command(pass_context=True, aliases=['code', 'source', 'git', 'github', 'scm'])
async def bot_code(ctx):
    """Link to source code GitHub repo."""
    await bot.say("https://github.com/tabrett/discord-multi-bot")


@bot.command(pass_context=True, aliases=['docs', 'apidocs'])
async def bot_docs(ctx):
    """Link to Discord.py API reference docs."""
    await bot.say("https://discordpy.readthedocs.io/en/latest/index.html")

#=========================
# non-command listeners
#=========================
@bot.event
async def on_message(message):

    # if bot in silent mode, only accept '!silent' command
    if config.SILENT_MODE:
        if message.startswith('!silent'):
            await bot.process_commands(message)
        return

    await bot.process_commands(message)                                         # allow commands to be processed first

    if message.author == bot.user:
        return 

    if message.mention_everyone:
        time.sleep(config.BOT_RESPONSE_DELAY)
        await bot.add_reaction(message, u'\U0001F621')
        await bot.send_message(message.channel, 
                              (random.choice(config.AT_EVERYONE_RESPONSES) 
                                          % (message.author.id)))

    if bot.user in message.mentions:
        await bot.send_message(message.channel, "Hi.")
    # print(message)

@bot.event
async def on_ready():
    print('Logged in as ', bot.user.name, bot.user.id, bot.user.bot)


#=========================
# run bot
#=========================
bot.run(config._BOT_TOKEN)