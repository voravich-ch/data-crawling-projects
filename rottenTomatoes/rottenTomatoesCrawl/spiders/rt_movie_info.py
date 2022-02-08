import scrapy
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
        urls = [f'https://www.rottentomatoes.com/m/{i}' for i in ids]
    else:
        urls = []
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_movie_urls(parent_dir_path)

# xpaths
rt_title_xpath = '//h1[@slot="title"]'
rt_user_rating_xpath = '//score-board/@audiencescore'
rt_cr_rating_xpath = '//score-board/@tomatometerscore'
rt_movie_desc_xpath = '//div[@id="movieSynopsis"]'
rt_genre_xpath = '//div[@class="meta-value genre"]'
rt_director_xpath = '//div[text()=\'Director:\']/following-sibling::div'
rt_producer_xpath = '//div[text()=\'Producer:\']/following-sibling::div'
rt_writer_xpath = '//div[text()=\'Writer:\']/following-sibling::div'
rt_release_date_th_xpath = '//div[text()=\'Release Date (Theaters):\']/following-sibling::div/time'
rt_release_date_st_xpath = '//div[text()=\'Release Date (Streaming):\']/following-sibling::div/time'
rt_gross_us_xpath = '//div[text()=\'Box Office (Gross USA):\']/following-sibling::div'
rt_production_xpath = '//div[text()=\'Production Co:\']/following-sibling::div'

class rtMovieInfoSpider(scrapy.Spider):
    name = 'rt_movie_info'
    allowed_domains = ['web']
    start_urls = urls

    def parse(self, response):    
        # create the loader
        l = ItemLoader(item = rottenTomatoesItem(), response = response)
        
        # key
        l.add_value('rt_tconst', re.search(r'([^\/]+)$', response.url).group(1))
        
        # primary fields
        l.add_xpath('rt_title', rt_title_xpath)
        l.add_xpath('rt_user_rating', rt_user_rating_xpath)
        l.add_xpath('rt_cr_rating', rt_cr_rating_xpath)
        l.add_xpath('rt_movie_desc', rt_movie_desc_xpath)
        l.add_xpath('rt_genre', rt_genre_xpath)
        l.add_xpath('rt_director', rt_director_xpath)
        l.add_xpath('rt_producer', rt_producer_xpath)
        l.add_xpath('rt_writer', rt_writer_xpath)
        l.add_xpath('rt_release_date_th', rt_release_date_th_xpath)
        l.add_xpath('rt_release_date_st', rt_release_date_st_xpath)
        l.add_xpath('rt_gross_us', rt_gross_us_xpath)
        l.add_xpath('rt_production', rt_production_xpath)
        
        # housekeeping fields
        l.add_value('url', response.url)
        l.add_value('spider', self.name)
        l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()

