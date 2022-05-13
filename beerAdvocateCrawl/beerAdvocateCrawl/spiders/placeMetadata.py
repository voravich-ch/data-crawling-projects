import scrapy
from beerAdvocateCrawl.items import beerAdvocateCrawlItem
from scrapy.loader import ItemLoader
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
    urls = [f'{base_url}{_id}' for _id in ids]
    return urls

# Parameters preparation
urls = populate_url()
# Xpath
name_xpath = '//h1/text()'
type_xpath = '//div[@id="info_box"]//text()[2]'
location_xpath = '//div[@id="info_box"]//text()'
gmap_xpath = '//a[contains(@href,"maps.google.com")]/@href'
is_active_xpath = '//span[text()="Closed"]'
stats_xpath = '//*[text()="PLACE STATS"]/parent::div//following-sibling::dd//text()'
beer_stats_xpath = '//*[text()="BEER STATS"]/parent::div//following-sibling::dd//text()'
phone_number_xpath = '//div[@id="info_box"]//text()'
website_xpath = '//div[@id="info_box"]//a[contains(text(), ".")]/@href'
notes_xpath = '//div[@id="info_box"]//text()'

class PlaceMetadataSpider(scrapy.Spider):
    name = 'placeMetadata'
    allowed_domains = ['beeradvocate.com']
    start_urls = urls

    def parse(self, response):
        # Create loader
        l = ItemLoader(item=beerAdvocateCrawlItem(), response=response)
        
        # Primary fields
        l.add_xpath('name', name_xpath)
        l.add_xpath('type', type_xpath)
        l.add_xpath('location', location_xpath)
        l.add_xpath('gmap', gmap_xpath)
        l.add_value('is_active', False if response.xpath(is_active_xpath) else True)
        l.add_xpath('stats', stats_xpath)
        l.add_xpath('beer_stats', beer_stats_xpath)
        l.add_xpath('phone_number', phone_number_xpath)
        l.add_xpath('website', website_xpath)
        l.add_xpath('notes', notes_xpath)
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()