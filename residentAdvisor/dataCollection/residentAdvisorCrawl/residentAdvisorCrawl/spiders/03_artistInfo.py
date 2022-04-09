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
        # Get artist urls
        urls = df['artist_url']
        # Remove null values – df contains one-hot data: clubs/events/artists
        urls = urls[~urls.isna()]
    else:
        urls = []
    return urls

# Parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_urls(parent_dir_path)

# Setting up XPath
artist_name_xpath = '//h1/span/text()'
artist_real_name_xpath = '//span[text()="Real name"]/following::span[1]/text()'
artist_alias_xpath = '//span[text()="Aliases"]/following::span[1]/text()'
artist_location_xpath = '//span[text()="Location"]/following::span[1]/text()'
artist_links_xpath = '//span[text()="Links"]/following::div[1]//a/@href'
artist_followers_xpath = '//span[text()="Followers"]/following::span[1]/text()'
artist_first_event_year_xpath = '//span[text()="First event on RA"]/following::span[1]/text()'
artist_region_most_played_xpath = '//span[text()="Regions most played"]/following::div[1]//a/@href'
artist_club_most_played_xpath = '//span[text()="Clubs most played"]/following::div[1]//a/@href'
artist_related_artists_xpath = '//h2[text()="Related Artists"]/following::div[1]//div/a/@href'
artist_labels_xpath = '//span[text()="Labels"]/following::div[1]//div/a/@href'

class artistInfoSpider(scrapy.Spider):
    name = '03_artistInfo'
    allowed_domains = ['ra.co']
    start_urls = list(urls)

    def parse(self, response):
        # Create loader
        l = ItemLoader(item=residentAdvisorItem(), response=response)
        
        # Primary fields
        l.add_xpath('artist_name', artist_name_xpath)
        l.add_xpath('artist_real_name', artist_real_name_xpath)
        l.add_xpath('artist_alias', artist_alias_xpath)
        l.add_xpath('artist_location', artist_location_xpath)
        l.add_xpath('artist_links', artist_links_xpath)
        l.add_xpath('artist_followers', artist_followers_xpath)
        l.add_xpath('artist_first_event_year', artist_first_event_year_xpath)
        l.add_xpath('artist_region_most_played', artist_region_most_played_xpath)
        l.add_xpath('artist_club_most_played', artist_club_most_played_xpath)
        l.add_xpath('artist_related_artists', artist_related_artists_xpath)
        l.add_xpath('artist_labels', artist_labels_xpath)
        # Key fields
        l.add_value('artist_id', re.search(r'https://ra.co(.+)', response.url).group(1))
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()
