from discord import Embed
from random import seed, randint

from .config import Config as config

def build_roll_result(author, diceVal, diceCount, hitCap=False):
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
