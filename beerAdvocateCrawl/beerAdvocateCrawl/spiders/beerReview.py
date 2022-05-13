import scrapy
from beerAdvocateCrawl.items import beerAdvocateCrawlItem
from scrapy.loader import ItemLoader
import os
import datetime
from urllib.parse import urljoin
from scrapy.http import FormRequest
from dotenv import load_dotenv
import pymongo

def get_beer_review_urls():
    client = pymongo.MongoClient()
    collection = client['beerAdvocate']['beerMetadata']
    cursor = collection.find({}, projection = {"_id": 0, "response_url": 1})
    beer_review_urls = [url['response_url'] for url in cursor]
    return beer_review_urls

# Parameter preparation
beer_review_urls = get_beer_review_urls()
# Load credentials
load_dotenv()

# Xpath
beer_xpath = '//h1/text()'
items_xpath = '//div[@id="rating_fullview_content_2"]'
author_xpath = './/a[@class="username"]'
date_xpath = './/span/a[@href]/text()'
rating_xpath = './/text()'
rDev_xpath = './/span[@style]/text()'
assessment_xpath = './/span[contains(text(), "|")]/text()'
text_xpath = './/text()'

class BeerReviewSpider(scrapy.Spider):
    name = 'beerReview'
    allowed_domains = ['beeradvocate.com']
    start_urls = ('https://www.beeradvocate.com/community/login/',)
    
    # Login
    def parse(self, response):
        return FormRequest.from_response(response,
                                         formdata={"login": os.environ.get('user'),
                                                   "password": os.environ.get('password')},
                                         callback=self.redirect
        )
    
    # Redirect to the page after login
    def redirect(self, response):
        for url in beer_review_urls:
            yield scrapy.Request(url=url,
                                callback=self.parse_item1,
                                dont_filter = True)
    
    # Horizontal Crawling 
    def parse_item1(self, response):
        # Parse data
        yield scrapy.Request(url=response.url,
                             callback=self.parse_item2)
        # If next review page exists
        if response.xpath('//a[text()="next"]/@href'):
            # Parse the next page url and fetch
            href = response.xpath('//a[text()="next"]/@href').extract_first()
            fetch_url = urljoin('https://www.beeradvocate.com', href)
            yield scrapy.Request(url=fetch_url,
                                 callback=self.parse_item1,
                                 dont_filter = True)
    
    # Parse data
    def parse_item2(self, response):
        # List of items
        items = response.xpath(items_xpath)
        
        for item in items:
            # Create loader
            l = ItemLoader(item=beerAdvocateCrawlItem(), selector=item)
            
            # Primary fields
            l.add_xpath('beer', beer_xpath)
            l.add_xpath('author', author_xpath)
            l.add_xpath('date', date_xpath)
            l.add_xpath('rating', rating_xpath)
            l.add_xpath('rDev', rDev_xpath)
            l.add_xpath('assessment', assessment_xpath)
            l.add_xpath('text', text_xpath)
            
            # Housekeeping fields
            l.add_value('response_url', response.url)
            l.add_value('spider', self.name)
            l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
            
            yield l.load_item()
