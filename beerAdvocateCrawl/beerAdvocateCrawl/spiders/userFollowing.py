import scrapy
from beerAdvocateCrawl.items import beerAdvocateCrawlItem
from scrapy.loader import ItemLoader
import os
import datetime
from urllib.parse import urljoin
from scrapy.http import FormRequest
from dotenv import load_dotenv

def populate_url():
    # Specify the base url
    base_url = 'https://www.beeradvocate.com/community/members/'
    # Specify min-max place ids
    # range = [1, 1332800)
    min_id = 1
    max_id = 1332800
    # Create a range of place ids
    ids = range(min_id, max_id)
    # Populate urls
    urls = [f'{base_url}{_id}/following?page=1' for _id in ids]
    return urls

# Parameters preparation
urls = populate_url()
# Load credentials
load_dotenv()

# Xpath
focal_xpath = '//span[@class="crust"]/a//text()'
followings_xpath = '//h3[@class="username"]//a/@href'

class UserFollowingSpider(scrapy.Spider):
    name = 'userFollowing'
    allowed_domains = ['beeradvocate.com']
    start_urls = ('https://www.beeradvocate.com/community/login/',)
    
    # Login
    def parse(self, response):
        return FormRequest.from_response(response,
                                         formdata={"login": os.environ.get('user'),
                                                   "password": os.environ.get('password')},
                                         callback=self.redirect)
    
    # Redirect to the page after login
    def redirect(self, response):
        for url in urls:
            yield scrapy.Request(url=url,
                                callback=self.parse_item1,
                                dont_filter = True)
    
    # Horizontal Crawling 
    def parse_item1(self, response):
        # Parse data
        yield scrapy.Request(url=response.url,
                             callback=self.parse_item2)
        # If next review page exists
        if response.xpath('//div[@class="sectionFooter"]//a[contains(@class, "button")]/@href'):
            # Parse the next page url and fetch
            href = response.xpath('//div[@class="sectionFooter"]//a[contains(@class, "button")]/@href').extract_first()
            fetch_url = urljoin('https://www.beeradvocate.com/community/', href)
            yield scrapy.Request(url=fetch_url,
                                 callback=self.parse_item1,
                                 dont_filter = True)
    
    # Parse data
    def parse_item2(self, response):
        # Create loader
        l = ItemLoader(item=beerAdvocateCrawlItem(), response=response)
        
        # Primary fields
        l.add_xpath('focal', focal_xpath)
        l.add_xpath('followings', followings_xpath)
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        yield l.load_item()
