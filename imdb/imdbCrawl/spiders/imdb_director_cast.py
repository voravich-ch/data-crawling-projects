import scrapy
from imdbCrawl.items import imdbItem
from scrapy.loader import ItemLoader

import os
import re
import datetime
import pandas as pd

from imdbCrawl.modules import get_parent_dir_path

def get_urls(parent_dir_path):
    # set file path
    folder = 'data'
    in_file = 'sample.json'
    target = os.path.join(parent_dir_path, folder, in_file) 
    # load file
    df = pd.read_json(target, orient='records')
    # get movie id
    ids = df.loc[:, 'tconst'].to_list()
    # get movie url
    urls = [f'https://www.imdb.com/title/{i}/fullcredits' for i in ids]
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_urls(parent_dir_path)

# xpaths
imdb_director_xpath = '//a[contains(@href, "dr")]'
imdb_cast_xpath = '//td[not(@class)]/a'

class imdbDirectorCastSpider(scrapy.Spider):
    name = 'imdb_director_cast'
    allowed_domains = ['web']
    start_urls = urls

    def parse(self, response):
        # create the loader
        l = ItemLoader(item = imdbItem(), response = response)
        
        # key
        l.add_value('imdb_tconst', re.search(r'\/(tt.+)\/', response.url).group(1))
        
        # primary fields
        l.add_xpath('imdb_director', imdb_director_xpath)
        l.add_xpath('imdb_cast', imdb_cast_xpath)
        
        # housekeeping fields
        l.add_value('url', response.url)
        l.add_value('spider', self.name)
        l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()