import scrapy
from metacriticCrawl.items import metacriticItem
from scrapy.loader import ItemLoader

import os
import re
import datetime
import pandas as pd

from metacriticCrawl.modules import get_parent_dir_path

def get_movie_urls(parent_dir_path):
    # set file path
    folder = 'data'
    in_file = 'mt_movie_url.jl'
    target = os.path.join(parent_dir_path, folder, in_file)
    # since the file was created from another spider -- debug spider problem
    # only load data if the file exists
    if os.path.isfile(target):
        # load file
        df = pd.read_json(target, lines=True)
        # get urls
        ids = df['mt_tconst']
        # get movie url
        urls = [f'https://www.metacritic.com/movie/{i}' for i in ids]
    else:
        urls = []
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_movie_urls(parent_dir_path)

# xpaths
mt_director_xpath = '//div[@class="director"]//span[not(@class)]'
mt_cast_xpath = '//div[@class="summary_cast details_section"]//a'

class mtDirectorCastSpider(scrapy.Spider):
    name = 'mt_director_cast'
    allowed_domains = ['web']
    start_urls = urls

    def parse(self, response): 
        # create the loader
        l = ItemLoader(item = metacriticItem(), response = response)
        
        # key
        l.add_value('mt_tconst', re.search(r'([^\/]+)$', response.url).group(1))
        
        # primary fields
        l.add_xpath('mt_director', mt_director_xpath)
        l.add_xpath('mt_cast', mt_cast_xpath)
        
        # housekeeping fields
        l.add_value('url', response.url)
        l.add_value('spider', self.name)
        l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()

