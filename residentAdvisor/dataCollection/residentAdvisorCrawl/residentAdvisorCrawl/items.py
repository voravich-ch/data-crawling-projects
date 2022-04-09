# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import json
from itemloaders.processors import MapCompose, Join, TakeFirst
from w3lib.html import remove_tags

def parse_gmap_url(url):
    """
    The google map urls that contain '%20' were decoded to a space character.
    This function parses back to make a valid url.
    """
    # Replace ' ' with '%20'
    output = url.replace(' ', '%20')
    return output

class residentAdvisorItem(scrapy.Item):
    # Duplicated fields (for documentation purposes) were indented out as only one is sufficient
    # Sitemap
    club_url = scrapy.Field(output_processor=TakeFirst())
    event_url = scrapy.Field(output_processor=TakeFirst())
    artist_url = scrapy.Field(output_processor=TakeFirst())
    
    # -----------
    # ClubInfo
    club_is_closed = scrapy.Field(input_processor=MapCompose(bool), output_processor=TakeFirst())
    club_name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    club_address = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    club_phone = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    club_website = scrapy.Field(output_processor=TakeFirst())
    club_gmap = scrapy.Field(input_processor=MapCompose(parse_gmap_url), output_processor=TakeFirst())
    club_location = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    club_followers = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    club_about = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    club_capacity = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    club_most_listed_artist = scrapy.Field() # Stored as list
    # -- keys
    club_id = scrapy.Field(output_processor=TakeFirst())
    
    # -----------
    # EventInfo
    event_name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # club_name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # club_address = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # club_location = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    event_date = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    event_time = scrapy.Field(input_processor=MapCompose(str.strip) , output_processor=Join(' '))
    event_promoters = scrapy.Field() # Stored as list
    event_attending = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    event_is_ra_pick = scrapy.Field(input_processor=MapCompose(bool), output_processor=TakeFirst())
    event_ra_comment = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    ra_name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst()) # Compose into URL for profile page: e.g., https://ra.co/profile/katiethomas for Katie Thomas
    event_lineup = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    event_detail = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    event_cost = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    event_min_age = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=Join(''))
    # -- keys
    # club_id = scrapy.Field(output_processor=TakeFirst())
    event_id = scrapy.Field(input_processor=MapCompose(lambda i: re.search(r"\d+", i).group(0)), output_processor=TakeFirst())
    event_artists = scrapy.Field() # Stored as list
    
    # -----------
    # ArtistInfo
    artist_name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    artist_real_name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    artist_alias = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst()) # Could be comma separated string
    artist_location = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    artist_links = scrapy.Field() # Stored as list
    artist_followers = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    artist_first_event_year = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    artist_region_most_played = scrapy.Field() # Stored as list
    artist_related_artists = scrapy.Field() # Stored as list
    artist_labels = scrapy.Field() # Stored as list
    # -- keys
    artist_id = scrapy.Field(output_processor=TakeFirst())
    artist_club_most_played = scrapy.Field() # Stored as list
    
    # -----------
    # Housekeeping fields
    response_url = scrapy.Field(output_processor=TakeFirst())
    spider = scrapy.Field(output_processor=TakeFirst())
    crawl_date = scrapy.Field(output_processor=TakeFirst())