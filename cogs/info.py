from discord import ( Embed )

from settings import config

def time_delta(dt):
    days = dt.days
    hrs, r = divmod(dt.seconds, 3600)
    mins, sec = divmod(r, 60)
    return (('Multibot has been active for: '
             '%s days, %s hours, %s minutes and %s seconds')
                % (days, hrs, mins, sec))



def build_InfoMessage():
    embed_title = 'Info for MultiBot'
    embed=Embed(title=embed_title)
    embed.add_field(name='Developed By', value='Taylor B.\t(taytay#6307)', inline=False)
    embed.add_field(name='Source Code', value='[GitHub](https://github.com/tabrett/discord-multi-bot)')
   #  embed.add_field(name='Hosted By', value='[Heroku](https://www.heroku.com/home)', inline=False)

    return embed
