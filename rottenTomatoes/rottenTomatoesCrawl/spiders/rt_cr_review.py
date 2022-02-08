import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from rottenTomatoesCrawl.items import rottenTomatoesItem
from scrapy.loader import ItemLoader

import os
import re
import datetime
import pandas as pd

from rottenTomatoesCrawl.modules import get_parent_dir_path

def get_movie_urls(parent_dir_path):
    # set file path
    folder = 'data'
    in_file = 'rt_movie_url.jl'
    target = os.path.join(parent_dir_path, folder, in_file)
    # since the file was created from another spider -- debug spider problem
    # only load data if the file exists
    if os.path.isfile(target):
        # load file
        df = pd.read_json(target, lines=True)
        # get urls
        ids = df['rt_tconst']
        # get movie url
        urls = [f'https://www.rottentomatoes.com/m/{i}/reviews' for i in ids]
    else:
        urls = []
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_movie_urls(parent_dir_path)

# xpaths
main_xpath = '//div[@class="row review_table_row"]'
rt_cr_xpath = './/div[contains(@class, "critic_name")]/a[1]'
rt_pub_xpath = './/div[contains(@class, "critic_name")]/a[2]'
rt_top_xpath = './/rt-icon-top-critic'
rt_fresh_xpath = './/div[contains(@class, "small fresh")]'
rt_cr_review_xpath = './/div[@class="the_review"]'
rt_cr_review_full_url_xpath = './/div[contains(@class, "review-link")]/a/@href'
rt_cr_review_date_xpath = './/div[contains(@class, "review-date")]'

class rtCrReviewSpider(CrawlSpider):
    name = 'rt_cr_review'
    allowed_domains = ['www.rottentomatoes.com']
    start_urls = urls
    
    # rules for horizontal crawling
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[contains(@data-qa, "next-btn")]'), 
             callback='parse_item', follow=True),
    )
    
    def parse_start_url(self, response):
        return self.parse_item(response)
    
    def parse_item(self, response):  
        # list of items
        main = response.xpath(main_xpath)
        
        for i in main:
            # create the loader
            l = ItemLoader(item = rottenTomatoesItem(), selector = i)
            
            # key
            l.add_value('rt_tconst', re.search(r'(\/m\/(.+))\/', response.url).group(2))
            
            # primary fields
            l.add_xpath('rt_cr', rt_cr_xpath)
            l.add_xpath('rt_pub', rt_pub_xpath)
            l.add_xpath('rt_top', rt_top_xpath)
            l.add_xpath('rt_fresh', rt_fresh_xpath)
            l.add_xpath('rt_cr_review', rt_cr_review_xpath)
            l.add_xpath('rt_cr_review_full_url', rt_cr_review_full_url_xpath)
            l.add_xpath('rt_cr_review_date', rt_cr_review_date_xpath)
            
            # housekeeping fields
            l.add_value('url', response.url)
            l.add_value('spider', self.name)
            l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
            
            yield l.load_item()

