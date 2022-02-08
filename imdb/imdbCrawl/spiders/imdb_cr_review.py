import scrapy
from imdbCrawl.items import imdbItem
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest

import os
import re
import datetime
import pandas as pd

from bs4 import BeautifulSoup
from bs4.element import Comment
from imdbCrawl.modules import get_parent_dir_path

def get_urls(parent_dir_path):
    # set file path
    folder = 'data'
    in_file = 'imdb_cr_url.jl'
    target = os.path.join(parent_dir_path, folder, in_file)
    # since the file was created from another spider -- debug spider problem
    # only load data if the file exists
    if os.path.isfile(target):
        # load file
        df = pd.read_json(target, lines=True)
        # get urls
        urls = df['imdb_cr_url']
    else:
        urls = []
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_urls(parent_dir_path)

# xpaths
imdb_cr_review_xpath = '//p/text()'

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

class imdbCrReviewSpider(scrapy.Spider):
    name = 'imdb_cr_review'
    allowed_domains = ['web']
    start_urls = list(urls)
    
    # Splash authentication
    http_user = 'user'
    http_pass = 'userpass'
    
    def start_requests(self):
        for url in self.start_urls:
            # render with Splash
            yield SplashRequest(url, self.parse, args={'wait': 2,
                                                       'timeout': 1800})

    def parse(self, response):    
        # create the loader
        l = ItemLoader(item = imdbItem(), response = response)
        
        all_text = text_from_html(response.body)
        
        # primary fields
        l.add_xpath('imdb_cr_review', imdb_cr_review_xpath)
        l.add_value('imdb_cr_review_all', all_text)
        
        # housekeeping fields
        l.add_value('url', response.url)
        l.add_value('spider', self.name)
        l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()

