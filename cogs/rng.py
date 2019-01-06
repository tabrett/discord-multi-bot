import asyncio
import aiohttp
import random
import re

from discord import ( Embed )
from random import ( randint, seed )

from settings.config import Config as config

def roll_parse(inputStr):
    # splits entry from !roll
    try: 
        lhs, rhs = inputStr.split(' ', 1)
    except ValueError:
        return 'help', 0

    if rhs in config.BOT_COMMANDS:
        # checks for alternate subcommand first
        return rhs, 0
    else:
        # attempts to break up the number of dice and type of dice to be rolled
        try: 
            sub_lhs, sub_rhs = rhs.split(' ', 1)
            if sub_lhs.lower() == 'max':
                return sub_rhs, config.ROLL_CAP
            else:
                return sub_rhs, sub_lhs
        except ValueError:
            try:
                sub_lhs, sub_rhs = rhs.split('x', 1)
                return sub_rhs, sub_lhs        
            except ValueError:
                try:
                    sub_lhs, sub_rhs = rhs.split('*', 1)
                    return sub_rhs, sub_lhs
                except ValueError:
                    try:
                        sub_lhs, sub_rhs = re.split(r'(?<=[0-9])d(?=[0-9])', rhs) 
                        return sub_rhs, sub_lhs
                    except ValueError:                    
                        return rhs, 1



def build_RollResult(author, diceVal, diceCount, hitCap=False):
    seed(randint(0, 9999999))
    total = 0
    embed_title = ('@%s\'s Roll Results of %sd%s' % (author, int(diceCount), int(diceVal)))
    embed=Embed(title=embed_title)
    embed.add_field(name=u"\u2015", value=u"\u200b", inline=False)
    for k in range(0, int(diceCount)):
        roll = randint(1, int(diceVal))
        roll_num = ('Roll #%s' % (k + 1))
        embed.add_field(name=roll_num, value=roll, inline=True)
        total += roll

    if diceCount > 1:
        embed.add_field(name=u"\u200b", value=u"\u200b", inline=False)
        embed.add_field(name='Total', value=total, inline=False)

    if hitCap:
        embed.set_footer(text='**You rolled too many dice.  This request has been capped at %s rolls.' 
                            % config.ROLL_CAP)

    return embed


def coin_flip():
    
    coin_faces = ['Heads','Tails']
    return random.choice(coin_faces)