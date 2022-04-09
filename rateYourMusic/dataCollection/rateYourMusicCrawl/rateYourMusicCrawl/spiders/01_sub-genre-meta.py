import scrapy
from scrapy.loader import ItemLoader
from rateYourMusicCrawl.items import rateYourMusicItem
import re
import datetime
import pymongo

def connect_to_city(db_name, collection_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    return collection

def get_urls(collection):
    cursor = collection.find({}, projection = {"_id": 0, "hierarchy": 1})
    # Get hrefs
    genres = [document['hierarchy'] for document in cursor]
    hrefs = [i['href'] for genre in genres for i in genre]
    # Format url
    urls = [f'https://rateyourmusic.com{href}' for href in hrefs]
    return urls

# Parameters preparations
collection = connect_to_city(db_name='rateYourMusic', collection_name='genre_hierarchy')
urls = get_urls(collection)

# Setting up XPath
genre_xpath = '//h1/text()'
n_release_xpath = '//div[@class="page_genre_akas"]/text()'
genre_description_xpath = '//span[@id="page_genre_description_full"]/span/text()'
related_descriptors_xpath = '//div[@class="page_genre_related_descriptors_content"]//span/text()'

class subGenreMetaSpider(scrapy.Spider):
    name = '01_sub-genre-meta'
    allowed_domains = ['rateyourmusic.com']
    start_urls = urls
    
    def parse(self, response):
        # Create loader
        l = ItemLoader(item=rateYourMusicItem(), response=response)
        
        # Primary fields
        l.add_xpath('genre', genre_xpath)
        l.add_xpath('n_release', n_release_xpath)
        l.add_xpath('genre_description', genre_description_xpath)
        l.add_xpath('related_descriptors', related_descriptors_xpath)
        l.add_value('top_level', 'No')
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()
