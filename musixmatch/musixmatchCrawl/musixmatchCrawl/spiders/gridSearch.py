import scrapy
from musixmatchCrawl.items import musixmatchItem
from scrapy.loader import ItemLoader
import datetime

def populate_url():
    # Specify the base url
    base_url = 'https://www.musixmatch.com/track'
    # Specify min-max track ids
    # range = [12,000,000 - 300,000,000] -- last `max_track` = 300000001
    # https://www.musixmatch.com/track/233106400
    # There were no track between 233106400 and 3500000000
    min_track = 12000000
    max_track = 300000001
    # Specify grid-size
    grid =  25000
    # Create a range of track ids with grid
    tracks = range(min_track, max_track, grid)
    # Populate urls
    urls = [f'{base_url}/{track}' for track in tracks]
    return urls

urls = populate_url()

class musixmatchSpider(scrapy.Spider):
    name = 'gridSearch4'
    allowed_domains = ['musixmatch.com']
    start_urls = urls
    
    def parse(self, response):
        # Create loader
        l = ItemLoader(item=musixmatchItem(), response=response)
        
        # Housekeeping fields
        l.add_value('request_url', response.request.meta['redirect_urls'])
        
        # print log
        print(self.crawler.stats.get_stats())
        
        return l.load_item()
