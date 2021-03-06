import requests
import urllib
import codecs

from pprint import pformat, pprint
from discord import Embed

from mediawiki import MediaWiki

wiki = MediaWiki()

def get_raw_page(title):
    title = title.replace(' ', '_')
    r = requests.get(('https://en.wikipedia.org/api/rest_v1/page/summary/%s'
                        % urllib.parse.quote_plus(title)))
    return r

def build_from_raw(wiki_payload):
    embed_title = wiki_payload['displaytitle']
    
    embed = Embed(title=embed_title)
    embed.add_field(name="Summary", 
                    value=wiki_payload['extract'], 
                    inline=True)
    
    embed.set_thumbnail(url=wiki_payload['thumbnail']['source'])
    embed.add_field(name="URL", 
                    value=wiki_payload['content_urls']['desktop']['page'],
                    inline=True)
    return embed


def get_wiki_page(title):
    wiki_search = wiki.search(title)[0]
    return wiki.page(wiki_search)
    

def build_wiki_embed(wiki_page):
    embed_title = wiki_page.title

    embed = Embed(title=embed_title)

    # TODO: How to fix decode of summary?
    #   Works on most pages, but pages like "Saint Patrick's Day" break.
    #   What exactly is causing it to break? 
    # decode_summary = wiki_page.summary.encode('ascii', 'ignore').decode('ascii')
    # decode_summary = decode_summary.replace("\"", '\'')
    # decode_summary = decode_summary.replace("\n", '')
    
    embed.add_field(name="Summary", value=wiki_page.summary, inline=True)
    
    embed.set_thumbnail(url=wiki_page.logos[0])
    embed.add_field(name="URL", 
                    value=wiki_page.url,
                    inline=True)
    return embed