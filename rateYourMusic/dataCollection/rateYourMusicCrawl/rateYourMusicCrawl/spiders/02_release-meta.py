import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from rateYourMusicCrawl.items import rateYourMusicItem
import re
import datetime
import pymongo

# def connect_to_city(db_name, collection_name):
#     client = pymongo.MongoClient()
#     db = client[db_name]
#     collection = db[collection_name]
#     return collection

# def get_urls(collection):
#     cursor = collection.find({}, projection = {"_id": 0, "hierarchy": 1})
#     # Get hrefs
#     genres = [document['hierarchy'] for document in cursor]
#     hrefs = [i['href'] for genre in genres for i in genre]
#     # Format url
#     urls = [f'https://rateyourmusic.com{href}' for href in hrefs]
#     return urls

# # Parameters preparations
# collection = connect_to_city(db_name='rateYourMusic', collection_name='genre_hierarchy')
# urls = get_urls(collection)

# Setting up XPath
release_id_xpath = '//div[@class="album_title"]/input/@value'
release_name_xpath = '//div[@class="album_title"]/text()'
artists_xpath = '//th[text()="Artist"]/following::span[@itemprop="byArtist"]//a[@class="artist"]'
release_type_xpath = '//th[text()="Type"]/following::td[1]/text()'
release_date_xpath = '//th[text()="Released"]/following::td[1]//text()'
rating_xpath = '//th[text()="RYM Rating"]/following::span[@class="avg_rating"]/text()'
n_ratings_xpath = '//th[text()="RYM Rating"]/following::span[@class="num_ratings"]/b/span/text()'
rank_xpath = '//th[text()="Ranked"]/following::td[1]//text()'
primary_genres_xpath = '//tr[@class="release_genres"]/td/div/span[@class="release_pri_genres"]//a/text()'
secondary_genres_xpath = '//tr[@class="release_genres"]/td/div/span[@class="release_sec_genres"]//a/text()'
descriptors_xpath = '//tr[@class="release_descriptors"]/td/div//span//text()'
language_xpath = '//th[text()="Languages " or text()="Language "]/following::td[1]//text()'

class subGenreLevelSpider(scrapy.Spider):
    name = '02_release-meta'
    allowed_domains = ['rateyourmusic.com']
    start_urls = ['https://rateyourmusic.com/release/single/new-order/temptation-hurt/',
                  'https://rateyourmusic.com/release/album/arjen-anthony-lucassens-star-one/revel-in-time/',
                  'https://rateyourmusic.com/release/album/%EC%95%BC%EC%95%BC-%ED%82%B4-yaya-kim/a_k_a-yaya/']
    
    def parse(self, response):
        # Create loader
        l = ItemLoader(item=rateYourMusicItem(), response=response)
        
        # Primary fields
        l.add_xpath('release_id', release_id_xpath)
        l.add_xpath('release_name', release_name_xpath)
        l.add_xpath('artists', artists_xpath)
        l.add_xpath('release_type', release_type_xpath)
        l.add_xpath('release_date', release_date_xpath)
        l.add_xpath('rating', rating_xpath)
        l.add_xpath('n_ratings', n_ratings_xpath)
        l.add_xpath('rank', rank_xpath)
        l.add_xpath('primary_genres', primary_genres_xpath)
        l.add_xpath('secondary_genres', secondary_genres_xpath)
        l.add_xpath('descriptors', descriptors_xpath)
        l.add_xpath('language', language_xpath)
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()
    
    # # Rules for horizontal crawling
    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//a[@class="ui_pagination_btn ui_pagination_next"]'), 
    #          callback='parse_item', follow=True),
    # )
    
    # def parse_start_url(self, response):
    #     return self.parse_item(response)
    
    # def parse_item(self, response):
    #     # Create loader
    #     l = ItemLoader(item=rateYourMusicItem(), response=response)
        
    #     # Primary fields
    #     l.add_xpath('genre', genre_xpath)
    #     l.add_xpath('genre_description', genre_description_xpath)
    #     l.add_xpath('hierarchy', hierarchy_xpath)
    #     l.add_xpath('related_descriptors', related_descriptors_xpath)
    #     l.add_xpath('hierarchy_structure', hierarchy_structure_xpath)
        
    #     # Housekeeping fields
    #     l.add_value('response_url', response.url)
    #     l.add_value('spider', self.name)
    #     l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
    #     return l.load_item()
