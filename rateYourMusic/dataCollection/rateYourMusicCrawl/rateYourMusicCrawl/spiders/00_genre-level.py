import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from rateYourMusicCrawl.items import rateYourMusicItem
import re
import datetime

# Setting up XPath
genre_xpath = '//h1/text()'
n_release_xpath = '//div[@class="page_genre_akas"]/text()'
genre_description_xpath = '//span[@id="page_genre_description_full"]/span//text()'
hierarchy_xpath = '//section[@id="page_genre_section_hierarchy"]//div/ul/li'
related_descriptors_xpath = '//div[@class="page_genre_related_descriptors_content"]//span/text()'
hierarchy_structure_xpath = hierarchy_xpath

class genreLevelSpider(CrawlSpider):
    name = '00_genre-level'
    allowed_domains = ['rateyourmusic.com']
    start_urls = (
        'https://rateyourmusic.com/genres/',
    )
    
    # Rules for vertical crawling
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2/a'), 
             callback='parse_item', follow=False),
    )
    
    def parse_item(self, response):
        # Create loader
        l = ItemLoader(item=rateYourMusicItem(), response=response)
        
        # Primary fields
        l.add_xpath('genre', genre_xpath)
        l.add_xpath('n_release', n_release_xpath)
        l.add_xpath('genre_description', genre_description_xpath)
        l.add_xpath('hierarchy', hierarchy_xpath)
        l.add_xpath('related_descriptors', related_descriptors_xpath)
        l.add_xpath('hierarchy_structure', hierarchy_structure_xpath)
        l.add_value('top_level', 'Yes')
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()
