import requests
import urllib

from pprint import pformat, pprint

def get_wiki_page(title):
    title = title.replace(' ', '_')
    return requests.get(('https://en.wiipedia.org/api/rest_v1/page/summary/%s'
                            % urllib.parse.quote_plus(title)))

                            


