# The goal of this spider is to collect data on "Who sampled Who in the music industry"
# Relevant song level attributes includes: album, release year, and tag

# Note: 
# If a song contains samples or was sampled by more than 3 songs, 
# a visit to href: /samples or /sampled is necessary to collect all the connections.
# For sample pages, one page contains 16 items. 

# There are three types of connections: sample / cover / remix

import scrapy
from whoSampledCrawl.items import whoSampledCrawlItem
from scrapy.loader import ItemLoader
import datetime
import pymongo

def get_track_url():
    client = pymongo.MongoClient()
    db = client['whoSampled']
    collection = db['trackURL']
    track_urls = [i['url'] for i in collection.find({}, projection = {"_id": 0, "url": 1})]
    return track_urls

track_urls = get_track_url()

# Setting up XPath
song_name_xpath = '//h1/text()'
artists_xpath = '//span[@class="trackArtistNames"]//a'
artists_raw_text_xpath = '//span[@class="trackArtistNames"]//text()'
album_name_xpath = '//h3[@class="release-name"]//a'
release_year_xpath = '//h3[contains(@itemprop, "Release")]/a/text()'
producers_xpath = '//span[@itemprop="producer"]//a'
genre_xpath = '//a[contains(@href, "genre")]'
tags_xpath = '//span[@itemprop="keywords"]//a'
n_sample_xpath = '//span[contains(text(), "Contains samples of")]/text()'
n_sampled_xpath = '//span[contains(text(), "Was sampled in")]/text()'
samples_xpath = '//span[contains(text(), "Contains samples of")]/ancestor::section/div/div'
sampled_xpath = '//span[contains(text(), "Was sampled in")]/ancestor::section/div/div'

class whoSampledSpider(scrapy.Spider):
    name = 'first-step-whoSampled'
    allowed_domains = ['whosampled.com']
    start_urls = track_urls
    
    def parse(self, response):
        # Create itemloader
        l = ItemLoader(item=whoSampledCrawlItem(), response=response)
        
        # Primary fields
        l.add_xpath('song_name', song_name_xpath)
        l.add_xpath('artists', artists_xpath)
        l.add_xpath('artists_raw_text', artists_raw_text_xpath)
        l.add_xpath('album_name', album_name_xpath)
        l.add_xpath('release_year', release_year_xpath)
        l.add_xpath('producers', producers_xpath)
        l.add_xpath('genre', genre_xpath)
        l.add_xpath('tags', tags_xpath)
        l.add_xpath('n_sample', n_sample_xpath)
        l.add_xpath('n_sampled', n_sampled_xpath)
        l.add_xpath('samples', samples_xpath)
        l.add_xpath('sampled', sampled_xpath)
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()
