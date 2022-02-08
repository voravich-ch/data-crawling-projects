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
        urls = [f'https://www.metacritic.com/movie/{i}/user-reviews' for i in ids]
    else:
        urls = []
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_movie_urls(parent_dir_path)

# xpaths
mt_user_score_xpath = '//table[@class="score_wrapper"]//td[@class="num_wrapper"]/span'
mt_user_n_score_xpath = '//table[@class="score_wrapper"]//span[@class="score_description"]/span[@class="based_on"]'
mt_user_n_pos_xpath = '//td[@class="right"]//*[@class="chart_wrapper"]'
mt_user_n_neg_xpath = '//td[@class="right"]//*[@class="chart_wrapper"]'
mt_user_n_mixed_xpath = '//td[@class="right"]//*[@class="chart_wrapper"]'


class mtUserScoreSpider(scrapy.Spider):
    name = 'mt_user_score'
    allowed_domains = ['web']
    start_urls = urls

    def parse(self, response):    
        # create the loader using the response
        l = ItemLoader(item = metacriticItem(), response = response)
        
        # key
        l.add_value('mt_tconst', re.search(r'(\/movie\/(.+))\/', response.url).group(2))
        
        # primary fields
        l.add_xpath('mt_user_score', mt_user_score_xpath)
        l.add_xpath('mt_user_n_score', mt_user_n_score_xpath)
        l.add_xpath('mt_user_n_pos', mt_user_n_pos_xpath)
        l.add_xpath('mt_user_n_neg', mt_user_n_neg_xpath)
        l.add_xpath('mt_user_n_mixed', mt_user_n_mixed_xpath)

        
        # housekeeping fields
        l.add_value('url', response.url)
        l.add_value('spider', self.name)
        l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()

