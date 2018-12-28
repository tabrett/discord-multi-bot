from discord import ( Embed )
import asyncio
import aiohttp

from settings import config

def build_HelpMessage():
    # this was a questionable decision at best
    help_dict = { '1': ('!roll 20', 'Rolls 1 d20'),
                  '2': ('!roll 2 20', 'Rolls 2 d20'),
                  '3': ('!roll 4x12', 'Rolls 4 d12'),
                  '4': ('!roll 6d10', 'Rolls 6 d10'), 
                  '5': ('!roll 12*4', 'Rolls 12 d4'), 
                  '6': ('!roll max 8', 'Rolls max amount of d8'),
                  '7': ('!michaelbot', 'Responds just like Michael.'), 
                  '8': ('!grantbot', 'Responds just like Grant.'),
                  '9': ('!roll info', 'Provides more info about the bot.') }

    for k, v in help_dict.items():
        lhs_max, rhs_max = 0, 0
        if len(v[0]) > lhs_max:
            lhs_max = len(v[0])
        
        if len(v[1]) > rhs_max:
            rhs_max = len(v[1])
    
    left_row_border, right_row_border = '', ''

    for i in range(0, (lhs_max + 2)):
        left_row_border = left_row_border + u'\u2550'

    for i in range(0, (rhs_max + 2)):
        right_row_border = right_row_border + u'\u2550'

    top_row_border = ( u'\u2554' + left_row_border + u'\u2566' 
                        + right_row_border + u'\u2557' )

    mid_row_border = ( u'\u2560' + left_row_border + u'\u256C' 
                        + right_row_border + u'\u2563' )

    bot_row_border = ( u'\u2560' + left_row_border + u'\u2569' 
                        + right_row_border + u'\u2563' )

    alt_bot_row = ( u'\u255A' + left_row_border + u'\u2550' 
                    + right_row_border + u'\u255D' )

    table_out = top_row_border + '\n'
    table_out += ( u'\u2551' + str(' Commands').ljust((lhs_max + 2), ' ')
                    + u'\u2551' + str(' Description').ljust((rhs_max + 2), ' ')
                    + u'\u2551' + '\n' )

    for k, v in help_dict.items():
        table_out += mid_row_border
        table_out +=  '\n'
        table_out += ( u'\u2551' + ' ' + v[0].ljust((lhs_max + 1), ' ')
                        + u'\u2551' + ' ' + v[1].ljust((rhs_max + 1), ' ')
                        + u'\u2551' + '\n' )

    table_out += bot_row_border
    table_out += '\n'
    table_out += ( u'\u2551' + '    ' 
                    + str('* Current maximum rolls: %s' % config.roll_cap).ljust((rhs_max + lhs_max + 1), ' ')
                    + u'\u2551' + '\n' )
                    
    table_out += alt_bot_row

    msg = '```\n' + table_out + '\n```'
    # msg = table_out
    return msg



def get_HelpImbed(message):
    embed_title = 'Below are some useful commands for MultiBot:'
    embed=Embed(title=embed_title)
    embed.add_field(name=u"\u200b", value='test output', inline=False)
    return embed
