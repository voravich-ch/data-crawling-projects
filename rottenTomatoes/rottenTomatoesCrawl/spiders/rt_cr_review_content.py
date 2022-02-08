import scrapy
from rottenTomatoesCrawl.items import rottenTomatoesItem
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
import os
import re
import datetime
import pandas as pd
import requests

from bs4 import BeautifulSoup
from bs4.element import Comment
from rottenTomatoesCrawl.modules import get_parent_dir_path

def get_parent_dir_path():
    # get the project directory name
    parent_dir = 'category-spanning'
    current_path = os.getcwd()
    # pattern: path end with 'category-spanning'
    pattern = r'.*category-spanning$'
    # get back by one level until arriving at the parent directory
    while not re.match(pattern=pattern, string=current_path):
        current_path = os.path.dirname(current_path)
    parent_dir_path = current_path
    return parent_dir_path

def get_urls(parent_dir_path):
    # set file path
    folder = 'data'
    in_file = 'rt_cr_review.jl'
    target = os.path.join(parent_dir_path, folder, in_file)
    # since the file was created from another spider -- debug spider problem
    # only load data if the file exists
    if os.path.isfile(target):
        # load file
        df = pd.read_json(target, lines=True)
        # get urls
        urls = df['rt_cr_review_full_url']
        # remove null values
        urls = [i for i in urls if str(i) != 'nan']
    else:
        urls = []
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_urls(parent_dir_path)

# xpaths
rt_cr_review_full_xpath = '//p'

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

class rtCrReviewContentSpider(scrapy.Spider):
    name = 'rt_cr_review_content'
    allowed_domains = ['web']
    start_urls = list(urls)
    
    # Splash authentication
    http_user = 'user'
    http_pass = 'userpass'
    
    def start_requests(self):
        for url in self.start_urls:
            # render with Splash
            yield SplashRequest(url, self.parse, args={'wait': 2,
                                                       'timeout': 10})
    
    def parse(self, response):
        # create the loader
        l = ItemLoader(item = rottenTomatoesItem(), response = response)
        
        all_text = text_from_html(response.body)
        
        # primary fields
        l.add_xpath('rt_cr_review_full', rt_cr_review_full_xpath)
        l.add_value('rt_cr_review_full_all', all_text)
        
        # housekeeping fields
        l.add_value('url', response.url)
        l.add_value('spider', self.name)
        l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
            
        return l.load_item()

