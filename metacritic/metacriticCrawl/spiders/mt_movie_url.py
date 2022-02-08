import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from metacriticCrawl.items import metacriticItem

import re
import datetime

# xpaths
main_xpath = '//div[@class = "title_bump"]//td[@class = "clamp-summary-wrap"]'
mt_url_xpath = './a/@href'

class mtMovieUrlSpider(CrawlSpider):
    name = 'mt_movie_url'
    allowed_domains = ['www.metacritic.com']
    start_urls = (
        'https://www.metacritic.com/browse/movies/score/metascore/all',
    )
    
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
            l.add_xpath('mt_tconst', mt_url_xpath,
                        MapCompose(lambda i: re.search(r'([^\/])+$', i).group(0)))
            
            # url field
            l.add_xpath('mt_url', mt_url_xpath)
            
            # housekeeping fields
            l.add_value('url', response.url)
            l.add_value('spider', self.name)
            l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
            
            yield l.load_item()
