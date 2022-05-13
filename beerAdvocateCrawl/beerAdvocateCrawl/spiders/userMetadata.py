import scrapy
from beerAdvocateCrawl.items import beerAdvocateCrawlItem
from scrapy.loader import ItemLoader
import os
import datetime
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
    urls = [f'{base_url}{_id}/#info' for _id in ids]
    return urls

# Parameters preparation
urls = populate_url()
# Load credentials
load_dotenv()

# Xpath
name_xpath = '//h1/text()'
status_xpath = '//p[@class="userBlurb"]//span[@class="userTitle"]/text()'
tags_xpath = '//div[@class="userBanners"]//strong/text()'
joined_date_xpath = '//*[text()="Joined:"]/parent::dl//following-sibling::dd//text()'
posts_done_xpath = '//div[@class="section infoBlock"]//*[text()="Posts:"]/parent::dl//following-sibling::dd//text()'
likes_received_xpath = '//*[text()="Likes Received:"]/parent::dl//following-sibling::dd//text()'
beer_karma_xpath = '//*[text()="Beer Karma: "]//following-sibling::a//text()'
info_beers_xpath = '//*[text()="Beers:"]/parent::dt/following-sibling::dd//text()'
info_places_xpath = '//*[text()="Places:"]/parent::dt/following-sibling::dd'
about_xpath = '//*[text()="About"]/parent::div/div/div//text()'
n_follower_xpath = '//*[text()="Followers"]/parent::h3/a/text()'
n_following_xpath = '//*[text()="Following"]/parent::h3/a/text()'

class UserMetadataSpider(scrapy.Spider):
    name = 'userMetadata'
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
        for url in urls:
            yield scrapy.Request(url=url,
                                callback=self.parse_item)   
    
    def parse_item(self, response):
        # Create loader
        l = ItemLoader(item=beerAdvocateCrawlItem(), response=response)
        
        # Primary fields
        l.add_xpath('name', name_xpath)
        l.add_xpath('status', status_xpath)
        l.add_xpath('tags', tags_xpath)
        l.add_xpath('joined_date', joined_date_xpath)
        l.add_xpath('posts_done', posts_done_xpath)
        l.add_xpath('likes_received', likes_received_xpath)
        l.add_xpath('beer_karma', beer_karma_xpath)
        l.add_xpath('info_beers', info_beers_xpath)
        l.add_xpath('info_places', info_places_xpath)
        l.add_xpath('about', about_xpath)
        l.add_xpath('n_follower', n_follower_xpath)
        l.add_xpath('n_following', n_following_xpath)
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()