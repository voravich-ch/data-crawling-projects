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
    urls = [f'https://www.imdb.com/title/{i}/externalreviews' for i in ids]
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_urls(parent_dir_path)

# xpaths
main_xpath = '//*[@id="external_reviews_content"]//a[contains(@class, "offsite")]'
imdb_cr_xpath = './text()'
imdb_cr_url_xpath = './@href'

class imdbCrUrlSpider(scrapy.Spider):
    name = 'imdb_cr_url'
    allowed_domains = ['web']
    start_urls = urls

    def parse(self, response):
        # list of items
        main = response.xpath(main_xpath)
        
        for i in main:
            # create the loader
            l = ItemLoader(item = imdbItem(), selector = i)
            
            # key
            l.add_value('imdb_tconst', re.search(r'\/(tt.+)\/', response.url).group(1))
            
            # primary fields
            l.add_xpath('imdb_cr', imdb_cr_xpath)
            l.add_xpath('imdb_cr_url',  imdb_cr_url_xpath)
            
            # housekeeping fields
            l.add_value('url', response.url)
            l.add_value('spider', self.name)
            l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
            
            yield l.load_item()