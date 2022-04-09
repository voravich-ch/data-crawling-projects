import scrapy
from residentAdvisorCrawl.items import residentAdvisorItem
from scrapy.loader import ItemLoader
import re
import datetime
import bs4
import requests
from w3lib.html import remove_tags

def get_sitemap_urls(url):
    # request the page
    response = requests.get(url)
    # parse html
    html_page = bs4.BeautifulSoup(response.content, 'html.parser')
    # get all urls
    urls = [url.get_text() for url in html_page.find_all('loc')]
    return urls

# Parameters preparations
urls = get_sitemap_urls('https://ra.co/sitemap.xml')

class sitemapSpider(scrapy.Spider):
    name = '00_sitemap'
    allowed_domains = ['ra.co']
    start_urls = urls
    
    def parse(self, response):
        # List of items
        html_page = bs4.BeautifulSoup(response.body, 'html.parser')
        items = html_page.find_all('loc')
        for i in items:
            # Parse into url format
            url = remove_tags(str(i))
            # Create loader
            l = ItemLoader(item=residentAdvisorItem())
            
            # Classify url into club/event/artist
            # -- club
            if re.fullmatch(pattern=r'https://ra.co/clubs/\w+', string=url):
                # Primary fields
                l.add_value('club_url', url)
                # housekeeping fields
                l.add_value('response_url', response.url)
                l.add_value('spider', self.name)
                l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
                yield l.load_item()
                
            # -- event
            if re.fullmatch(pattern=r'https://ra.co/events/\w+', string=url):
                # Primary fields
                l.add_value('event_url', url)
                # housekeeping fields
                l.add_value('response_url', response.url)
                l.add_value('spider', self.name)
                l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
                yield l.load_item()
                
            # -- artist
            if re.fullmatch(pattern=r'https://ra.co/dj/\w+', string=url):
                # Primary fields
                l.add_value('artist_url', url)
                # housekeeping fields
                l.add_value('response_url', response.url)
                l.add_value('spider', self.name)
                l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
                yield l.load_item()
