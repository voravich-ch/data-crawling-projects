import scrapy
from residentAdvisorCrawl.items import residentAdvisorItem
from scrapy.loader import ItemLoader
import os
import re
import datetime
import pandas as pd

def get_parent_dir_path():
    # Specify parent directory
    parent_dir = 'residentAdvisor'
    current_path = os.getcwd()
    # Pattern: path end with parent_dir name: ~./{parent_dir}
    pattern = f'.*{parent_dir}$'
    # Get back by one level until arriving at the parent directory
    while not re.match(pattern=pattern, string=current_path):
        current_path = os.path.dirname(current_path)
    parent_dir_path = current_path
    return parent_dir_path

def get_urls(parent_dir_path):
    # Set file path
    folder = 'dataCollection'
    subfolder = 'data'
    in_file = '00_sitemap.jl'
    target = os.path.join(parent_dir_path, folder, subfolder, in_file)
    # Since the file was created from another spider 
    # -- debug by only load the data if the file exists
    if os.path.isfile(target):
        # Load file
        df = pd.read_json(target, lines=True)
        # Get club urls
        urls = df['club_url']
        # Remove null values – df contains one-hot data: clubs/events/artists
        urls = urls[~urls.isna()]
    else:
        urls = []
    return urls

# Parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_urls(parent_dir_path)

# Setting up XPath
club_is_closed_xpath = '//span[text()="This club is permanently closed"]'
club_name_xpath = '//h1/span/text()'
club_address_xpath = '//span[text()="Address"]/following::span[1]/text()'
club_phone_xpath = '//span[text()="Phone"]/following::span[1]/text()'
club_website_xpath = '//span[text()="Links"]/following::span[@href][1]/@href'
club_gmap_xpath = '//span[text()="Links"]/following::span[@href][2]/@href'
club_location_xpath = '//div[@class="Box-omzyfs-0 Alignment-sc-1fjm9oq-0 jyHIdG"]//span[contains(@data-tracking-id, "guide")]/text()'
club_followers_xpath = '//span[text()="Followers"]/following::span[1]/text()'
club_about_xpath = '//h2/following::ul/li/span/text()'
club_capacity_xpath = '//span[text()="Capacity"]/following::span[1]/text()'
club_most_listed_artist_xpath = '//span[text()="Most listed artists"]/following::div[1]//a/@href'

class clubInfoSpider(scrapy.Spider):
    name = '01_clubInfo'
    allowed_domains = ['ra.co']
    start_urls = list(urls)

    def parse(self, response):
        # Create loader
        l = ItemLoader(item=residentAdvisorItem(), response=response)
        
        # Primary fields
        l.add_xpath('club_is_closed', club_is_closed_xpath)
        l.add_xpath('club_name', club_name_xpath)
        l.add_xpath('club_address', club_address_xpath)
        l.add_xpath('club_phone', club_phone_xpath)
        l.add_xpath('club_website', club_website_xpath)
        l.add_xpath('club_gmap', club_gmap_xpath)
        l.add_xpath('club_location', club_location_xpath)
        l.add_xpath('club_followers', club_followers_xpath)
        l.add_xpath('club_about', club_about_xpath)
        l.add_xpath('club_capacity', club_capacity_xpath)
        l.add_xpath('club_most_listed_artist', club_most_listed_artist_xpath)
        
        # Key fields
        l.add_value('club_id', re.search(r'\d+', response.url).group(0))
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()
