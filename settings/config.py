# don't reveal to others
bot_token = 'BOT_TOKEN_HERE'
bot_key = "BOT_KEY_HERE"

# the absolute max is 21 due to embedded message limits
roll_cap = 15

# add or remove to include N-sided die to !roll command
valid_dice = [4, 6, 8, 10, 12, 16, 20, 100]

bot_commands = ['help','commands','info']

# responses are randomly chosen.  <@%s> replaced by user that uses @everyone
at_everyone_responses = [ 
                '<@%s> Wow, guy.',
                '<@%s> Don\'t @ me, please.',
                '<@%s> Wow wtf',
                '<@%s> No u',
                '<@%s> Don\'t fucking @ me, nerd.',
                'Hey @everyone, <@%s> is a jerk.',
                'Wow, <@%s>.  I can\'t believe you just used @everyone.',
                '<@%s> No.' ]
