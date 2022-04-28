import scrapy
from musixmatchCrawl.items import musixmatchItem
from scrapy.loader import ItemLoader
import datetime

def populate_url():
    # Specify the base url
    base_url = 'https://www.musixmatch.com/track'
    # Specify min-max track ids
    # range = [555,813, 233,106,400 ]
    min_track = 555813
    # max_track = 233,106,400 
    max_track= 240000000
    # Create a range of track ids
    tracks = range(min_track, max_track + 1)
    # Populate urls
    urls = [f'{base_url}/{track}' for track in tracks]
    # Define spider's name
    spd_name = f'{min_track}_{max_track}'
    return urls, spd_name

urls, spd_name = populate_url()

# Setting up XPath
# Variables XPath
var_xpath = '/html/body/script[1]/text()'

class musixmatchSpider(scrapy.Spider):
    name = spd_name
    allowed_domains = ['musixmatch.com']
    start_urls = urls
    
    def parse(self, response):
        # Create loader
        l = ItemLoader(item=musixmatchItem(), response=response)
        
        # Primary fields
        l.add_xpath('variables', var_xpath)
        
        # Housekeeping fields
        l.add_value('request_url', response.request.meta['redirect_urls'])
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        # print log
        print(self.crawler.stats.get_stats())
        
        return l.load_item()
