import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
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
main_xpath = '//div[@class="user_reviews"]//div[starts-with(@class, "review pad")]'
mt_user_xpath = './/span[@class="author"]'
mt_user_review_score_xpath = './/div[starts-with(@class, "metascore_w")]'
mt_user_review_date_xpath = './/span[@class="date"]'
mt_user_review_xpath = './/div[@class="review_body"]/span[not(@class)] | \
    .//div[@class="review_body"]//span[contains(@class, "expanded")]'


class mtUserReviewSpider(CrawlSpider):
    name = 'mt_user_review'
    allowed_domains = ['www.metacritic.com']
    start_urls = urls
    
    # rules for horizontal crawling
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]'), 
             callback='parse_item', follow=True),
    )
    
    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        # list of items
        main = response.xpath(main_xpath)
        
        for i in main:
            # create the loader
            l = ItemLoader(item = metacriticItem(), selector = i)
            
            # key
            l.add_value('mt_tconst', re.search(r'(\/movie\/(.+))\/', response.url).group(2))
            
            # primary fields
            l.add_xpath('mt_user', mt_user_xpath)
            l.add_xpath('mt_user_review_score', mt_user_review_score_xpath)
            l.add_xpath('mt_user_review_date', mt_user_review_date_xpath)
            l.add_xpath('mt_user_review', mt_user_review_xpath)
            
            # housekeeping fields
            l.add_value('url', response.url)
            l.add_value('spider', self.name)
            l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
            
            yield l.load_item()

