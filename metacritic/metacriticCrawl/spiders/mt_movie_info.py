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
mt_movie_name_xpath = '//div[@class="product_header"]//h1'
mt_genre_xpath = '//div[@class="genres"]//span[not(@class)]'
mt_movie_desc_xpath = '//div[contains(@class, "summary_deck")]//span'
mt_distributor_xpath = '//span[@class="distributor"]//a'
mt_release_date_xpath = '//span[@class="release_date"]/span[not(@class)]'
mt_user_n_review_xpath = '//a[@class="see_all boxed oswald" and contains(@href, "user-reviews")]'
mt_cr_n_review_xpath = '//a[@class="see_all boxed oswald" and contains(@href, "critic-reviews")]'

class mtMovieInfoSpider(scrapy.Spider):
    name = 'mt_movie_info'
    allowed_domains = ['web']
    start_urls = urls

    def parse(self, response):    
        # create the loader
        l = ItemLoader(item = metacriticItem(), response = response)
        
        # key
        l.add_value('mt_tconst', re.search(r'([^\/]+)$', response.url).group(1))
        
        # primary fields
        l.add_xpath('mt_movie_name', mt_movie_name_xpath)
        l.add_xpath('mt_genre', mt_genre_xpath)
        l.add_xpath('mt_movie_desc', mt_movie_desc_xpath)
        l.add_xpath('mt_distributor', mt_distributor_xpath)
        l.add_xpath('mt_release_date', mt_release_date_xpath)
        l.add_xpath('mt_user_n_review', mt_user_n_review_xpath)
        l.add_xpath('mt_cr_n_review', mt_cr_n_review_xpath)
        
        # housekeeping fields
        l.add_value('url', response.url)
        l.add_value('spider', self.name)
        l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()

