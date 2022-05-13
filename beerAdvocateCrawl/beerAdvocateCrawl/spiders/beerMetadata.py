import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from beerAdvocateCrawl.items import beerAdvocateCrawlItem
from scrapy.loader import ItemLoader
import os
import datetime

def populate_url():
    # Specify the base url
    base_url = 'https://www.beeradvocate.com/beer/profile/'
    # Specify min-max place ids
    # range = [1, 62000)
    min_id = 1
    max_id = 62000
    # Create a range of place ids
    ids = range(min_id, max_id)
    # Populate urls
    url_active = [f'{base_url}{_id}/#lists' for _id in ids]
    url_retired = [f'{base_url}{_id}/?show=retired#lists' for _id in ids]
    urls = url_active + url_retired
    return urls

# Parameters preparation
urls = populate_url()
# Xpath
name_xpath = '//h1/text()'
table_xpath = '//dl[@class="beerstats"]'
notes_xpath = '//b[text()="Notes:"]/parent::div//text()'

class BeerMetadataSpider(CrawlSpider):
    name = 'beerMetadata'
    allowed_domains = ['beeradvocate.com']
    start_urls = urls
    
    # Rules for vertical crawling
    rules = (
        Rule(LinkExtractor(allow=r'beer/profile/\d+/\d+/$'), 
             callback='parse_item', follow=False),
    )
    
    def parse_item(self, response):
        # Create loader
        l = ItemLoader(item=beerAdvocateCrawlItem(), response=response)
        
        # Primary fields
        l.add_xpath('name', name_xpath)
        l.add_xpath('company', table_xpath)
        l.add_xpath('style', table_xpath)
        l.add_xpath('ABV', table_xpath)
        l.add_xpath('score', table_xpath)
        l.add_xpath('avg', table_xpath)
        l.add_xpath('pDev', table_xpath)
        l.add_xpath('ratings', table_xpath)
        l.add_xpath('status', table_xpath)
        l.add_xpath('date_added', table_xpath)
        l.add_xpath('notes', notes_xpath)
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()