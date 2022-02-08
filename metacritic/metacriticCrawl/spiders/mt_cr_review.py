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
        urls = [f'https://www.metacritic.com/movie/{i}/critic-reviews' for i in ids]
    else:
        urls = []
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_movie_urls(parent_dir_path)

# xpaths
main_xpath = '//div[@class="list pad_top_half pad_btm1"]//div[starts-with(@class, "review")]'
mt_cr_xpath = './/div[@class="title pad_btm_half"]//img/@title | \
    .//div[@class="title pad_btm_half"]//span[@class="source" or @class="author"]'
mt_cr_review_score_xpath = './/div[starts-with(@class, "metascore_w")]'
mt_cr_review_date_xpath = './/div[@class="title pad_btm_half"]//span[@class="date"]'
mt_cr_review_xpath = './/div[@class="summary"]//a[@class="no_hover"]'
mt_cr_review_full_url_xpath = './/div[@class="summary"]//a[@class="read_full"]//@href'


class mtCrReviewSpider(scrapy.Spider):
    name = 'mt_cr_review'
    allowed_domains = ['web']
    start_urls = urls

    def parse(self, response):
        # list of items
        main = response.xpath(main_xpath)
        
        for i in main:
            # create the loader
            l = ItemLoader(item = metacriticItem(), selector = i)
            
            # key
            l.add_value('mt_tconst', re.search(r'(\/movie\/(.+))\/', response.url).group(2))
            
            # primary fields
            l.add_xpath('mt_cr', mt_cr_xpath)
            l.add_xpath('mt_cr_review_score', mt_cr_review_score_xpath)
            l.add_xpath('mt_cr_review_date', mt_cr_review_date_xpath)
            l.add_xpath('mt_cr_review', mt_cr_review_xpath)
            l.add_xpath('mt_cr_review_full_url', mt_cr_review_full_url_xpath)
            
            # housekeeping fields
            l.add_value('url', response.url)
            l.add_value('spider', self.name)
            l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
            
            yield l.load_item()

