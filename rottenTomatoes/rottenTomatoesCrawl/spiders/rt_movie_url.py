import scrapy
from scrapy.loader import ItemLoader
from rottenTomatoesCrawl.items import rottenTomatoesItem
from itemloaders.processors import MapCompose

import re
import datetime
import bs4
import requests

def get_sitemap_urls(url):
    # request the page
    response = requests.get(url)
    # parse html
    html_page = bs4.BeautifulSoup(response.content, 'html.parser')
    # get all urls
    urls = [url.get_text() for url in html_page.find_all('loc')]
    return urls

# parameters preparations
urls = get_sitemap_urls('https://www.rottentomatoes.com/sitemap.xml')

class rtMovieUrlSpider(scrapy.Spider):
    name = 'rt_movie_url'
    allowed_domains = ['www.rottentomatoes.com']
    start_urls = urls
    
    def parse(self, response):
        # list of items we want
        html_page = bs4.BeautifulSoup(response.body, 'html.parser')
        items = html_page.find_all('loc')
        for i in items:
            # convert the tag into string
            i = str(i)
            # create the loader using the response
            l = ItemLoader(item = rottenTomatoesItem(), selector = i)
            
            # extract url
            pattern = r'(https://www.rottentomatoes.com/m/.+?(?=\<))'
            if re.search(pattern, i):
                url = re.search(pattern, i).group(0)
                # filter only the page url not other components such as image -- url not have further extension: e.g. '/pictures'
                pattern = r'https://www.rottentomatoes.com/m/.+/'
                if re.search(pattern, url) is None:
                    # key
                    l.add_value('rt_tconst', url,
                                MapCompose(lambda i: re.search(r'([^\/])+$', i).group(0)))
                    
                    # primary field
                    l.add_value('rt_url', url)
                    
                    # housekeeping fields
                    l.add_value('url', response.url)
                    l.add_value('spider', self.name)
                    l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
                    
                    yield l.load_item()