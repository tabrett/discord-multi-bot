import os
class Config:

    # don't reveal to others
    
    if os.environ.get('DISCORD_BOT_TOKEN') is not None:
        _BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
    else: 
        # CHANGE THE VALUE BETWEEN QUOTES IF BOT WAS DOWNLOADED
        _BOT_TOKEN = 'BOT_TOKEN_HERE'

    # the absolute max is 21 due to embedded message limits, 15 is less arbitrary
    ROLL_CAP = 15

    # what each command begins with
    # other possibilities (not limited to these): ?, //, ~, >, >>, $
    COMMAND_PREFIX = '!'
    
    # add or remove to include N-sided die to !roll command
    VALID_DICE = [3, 4, 6, 8, 10, 12, 16, 20, 100]

    BOT_COMMANDS = ['help','commands','info']

    # responses are randomly chosen.  <@%s> replaced by user that uses @everyone
    AT_EVERYONE_RESPONSES = [ 
                    '<@%s> Wow, guy.',
                    '<@%s> Don\'t @ me, please.',
                    '<@%s> Wow wtf',
                    '<@%s> No u',
                    '<@%s> Don\'t fucking @ me, nerd.',
                    'Hey @everyone, <@%s> is a jerk.',
                    'Wow, <@%s>.  I can\'t believe you just used @everyone.',
                    '<@%s> No.',
                    ('<@%s> '
                     u'\U0001F621') ]

    # seconds of delay for some bot responses
    BOT_RESPONSE_DELAY = .3

    LANDING_CHANNEL_NAME = "General"
    TARGET_CHANNEL_NAME = "MoveHere"
