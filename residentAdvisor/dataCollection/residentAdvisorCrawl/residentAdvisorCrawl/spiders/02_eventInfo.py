import scrapy
from residentAdvisorCrawl.items import residentAdvisorItem
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
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
        # Get event urls
        urls = df['event_url']
        # Remove null values – df contains one-hot data: clubs/events/artists
        urls = urls[~urls.isna()]
    else:
        urls = []
    return urls

# Parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_urls(parent_dir_path)

# Parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_urls(parent_dir_path)

# Xpaths
event_name_xpath = '//h1/span/text()'
club_name_xpath = '//span[text()="Venue"]/following::span[1]/text()'
club_address_xpath = '//span[text()="Venue"]/following::span[2]/text()'
club_location_xpath = '//div[@class="Box-omzyfs-0 Alignment-sc-1fjm9oq-0 jyHIdG"]//span[contains(@data-tracking-id, "guide")]/text()'
event_date_xpath = '//span[text()="Date"]/following::span[1]/text()'
event_time_xpath = '//span[text()="Date"]/following::div[2]/span/text()'
event_promoters_xpath = '//span[text()="Promoters" or text()="Promoter"]//following::div[1]/a/@href'
event_attending_xpath = '//span[text()="Attending"]/following::span[1]/text()'
event_is_ra_pick_xpath = '//span[text()="RA Pick"]'
event_ra_comment_xpath = '//span[text()="RA PICK"]/following::span[1]/text()'
ra_name_xpath = '//span[text()="RA PICK"]/following::span[2]/text()'
event_lineup_xpath = '//h2[text()="Lineup"]/following::span[1]'
event_artists_xpath = '//h2[text()="Lineup"]/following::span[1]//a/@href'
event_detail_xpath = '//div[@class="Box-omzyfs-0 iGYDtd"]/span/text()'
event_cost_xpath = '//span[text()="Cost"]/following::span[1]/text()'
event_min_age_xpath = '//span[text()="Min. age"]/following::span[1]/text()'
club_id_xpath = '//span[text()="Venue"]/following::span[1]/@href'

class eventInfoSpider(scrapy.Spider):
    name = '02_eventInfo'
    allowed_domains = ['ra.co']
    start_urls = list(urls)

    def parse(self, response):
        # Create loader
        l = ItemLoader(item=residentAdvisorItem(), response=response)
        
        # Primary fields
        l.add_xpath('event_name', event_name_xpath)
        l.add_xpath('club_name', club_name_xpath)
        l.add_xpath('club_address', club_address_xpath)
        l.add_xpath('club_location', club_location_xpath)
        l.add_xpath('event_date', event_date_xpath)
        l.add_xpath('event_time', event_time_xpath)
        l.add_xpath('event_promoters', event_promoters_xpath)
        l.add_xpath('event_attending', event_attending_xpath)
        l.add_xpath('event_is_ra_pick', event_is_ra_pick_xpath)
        l.add_xpath('event_ra_comment', event_ra_comment_xpath)
        l.add_xpath('ra_name', ra_name_xpath)
        l.add_xpath('event_lineup', event_lineup_xpath)
        l.add_xpath('event_artists', event_artists_xpath)
        l.add_xpath('event_detail', event_detail_xpath)
        l.add_xpath('event_cost', event_cost_xpath)
        l.add_xpath('event_min_age', event_min_age_xpath)
        
        # Key fields
        l.add_xpath('club_id', club_id_xpath, MapCompose(lambda i: re.search(r"\d+", i).group(0)))
        l.add_value('event_id', re.search(r'\d+', response.url).group(0))
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()
