import scrapy
from imdbCrawl.items import imdbItem
from scrapy.loader import ItemLoader

import os
import re
import datetime
import pandas as pd

from imdbCrawl.modules import get_parent_dir_path

def get_movie_urls(parent_dir_path):
    # set file path
    folder = 'data'
    in_file = 'sample.json'
    target = os.path.join(parent_dir_path, folder, in_file) 
    # load file
    df = pd.read_json(target, orient='records')
    # get movie id
    ids = df.loc[:, 'tconst'].to_list()
    # get movie url
    urls = [f'https://www.imdb.com/title/{i}/' for i in ids]
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_movie_urls(parent_dir_path)

# xpaths
imdb_title_xpath = '//div[@class="title_wrapper"]//h1/text() | \
    //h1[contains(@class, "TitleHeader")]'
imdb_rating_xpath = '//div[@id="title-overview-widget"]//span[@itemprop="ratingValue"] | \
    //span[contains(@class, "RatingScore")]'
imdb_n_rating_xpath = '//script[@type="application/ld+json"]'
imdb_movie_desc_xpath = '//div[@id="title-overview-widget"]//div[@class="summary_text"] | \
    //div[contains(@data-testid, "plot-xl")]'
imdb_user_n_review_xpath = '//div[@id="title-overview-widget"]//a[starts-with(@href, "reviews")] | \
    //a[contains(@href, "/reviews")]//span[@class="three-Elements"]'
imdb_cr_n_review_xpath = '//div[@id="title-overview-widget"]//a[starts-with(@href, "externalreviews")] | \
    //a[contains(@href, "/externalreviews")]//span[@class="three-Elements"]'
imdb_budget_xpath = '//h4[text()="Budget:"]/following-sibling::text()[1] | \
    //li[contains(@data-testid, "budget")]'
imdb_gross_us_xpath = '//h4[text()="Gross USA:"]/following-sibling::text() | \
    //li[contains(@data-testid, "grossdomestic")]'
imdb_release_date_xpath = '//div[@id="title-overview-widget"]//div[@class="subtext"]//a[starts-with(@href, "/title")] | \
    //li[contains(@data-testid, "releasedate")]//li'

class imdbMovieInfoSpider(scrapy.Spider):
    name = 'imdb_movie_info'
    allowed_domains = ['web']
    start_urls = urls

    def parse(self, response):    
        # create the loader
        l = ItemLoader(item = imdbItem(), response = response)
        
        # key
        l.add_value('imdb_tconst', re.search(r'([^\/]+)[\/]$', response.url).group(1))
        
        # primary fields
        l.add_xpath('imdb_title', imdb_title_xpath)
        l.add_xpath('imdb_rating', imdb_rating_xpath)
        l.add_xpath('imdb_n_rating', imdb_n_rating_xpath)
        l.add_xpath('imdb_movie_desc', imdb_movie_desc_xpath)
        l.add_xpath('imdb_user_n_review', imdb_user_n_review_xpath)
        l.add_xpath('imdb_cr_n_review', imdb_cr_n_review_xpath)
        l.add_xpath('imdb_budget', imdb_budget_xpath)
        l.add_xpath('imdb_gross_us', imdb_gross_us_xpath)
        l.add_xpath('imdb_release_date', imdb_release_date_xpath)
        
        # housekeeping fields
        l.add_value('url', response.url)
        l.add_value('spider', self.name)
        l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()

