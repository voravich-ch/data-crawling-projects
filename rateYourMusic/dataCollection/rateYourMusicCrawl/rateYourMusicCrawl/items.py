# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import json
import numpy as np
from itemloaders.processors import MapCompose, Join, TakeFirst, Compose
import bs4

def parse_hierarchy(hierarchy):
    """
    Parse sub-genres in the hierarchy section into genre, description, href
        Example:
            [
                {
                    "genre": "Ambient Dub",
                    "description": "Fusion of Ambient and Dub reggae, featuring the atmosphere of the former and the Jamaican-style basslines, percussion, and psychedelic production techniques of the latter.",
                    "href": "/genre/ambient/"
                },
            ]
    """
    # Parse html
    html = bs4.BeautifulSoup(hierarchy, 'html.parser')
    # Find all items
    items = html.select('li[class="hierarchy_list_item"]')
    # Format data
    output = []
    for item in items:
        _dict = {
            "genre": item.find('a').get_text(strip=True),
            "description": item.find('p').get_text(strip=True),
            "href": item.find('a')['href']
        }
        output.append(_dict)
    return output

# def parse_hierarchy_structure(hierarchy_structure):
#     """
#     Parse genre hierarchy structure:
#         Example:
#             [
#                 {
#                     "genre": "Ambient Dub",
#                     "parent_genre": "Ambient",
#                     "top_level": "No"
#                 },
#             ]
#     """
#     # Parse html
#     html = bs4.BeautifulSoup(hierarchy_structure, 'html.parser')
#     # Get parent genre
#     parent = html.find('li', class_="hierarchy_list_item hierarchy_list_item_current").get_text(strip=True)
#     # Format data
#     output = {}
#     genre_list = [] # To skip sub-genres that were already parsed
#     # Insert parent genre
#     _parent = {
#         "parent_genre": None,
#         "top_level": "Yes"
#     }
#     output[parent] = _parent
#     genre_list.append(parent)
    
#     # Iterate over all items
#     _pass = 0 # Dummy for skipping duplicates sub-genres -- the structure is very complicated
#     items = html.select('li > ul > li[class="hierarchy_list_item"]')
#     for item in items:
#         genre = item.find('a').get_text(strip=True)
#         _dict = {
#                 "parent_genre": [parent],
#                 "top_level": "No"
#             }
#         if genre not in genre_list:
#             output[genre] = _dict
#             genre_list.append(genre)
#         # Check if there are sub-sub-genres
#         if item.find('ul'):
#             for i in item.find_all('ul'):
#                 if _pass == 0:
#                     if i.find_all('ul'):
#                         _pass = len(i.find_all('ul')) # To skip the next iterations
#                     genre = i.find('a').get_text(strip=True)
#                     _dict = {
#                         "parent_genre": [item.find('a').get_text(strip=True)],
#                         "top_level": "No"
#                     }
#                     if genre not in genre_list:
#                         output[genre] = _dict
#                         genre_list.append(genre)
#                     else:
#                         if item.find('a').get_text(strip=True) not in output[genre]['parent_genre']:
#                             output[genre]['parent_genre'].append(item.find('a').get_text(strip=True))
#                 elif _pass > 0:
#                     _pass = _pass - 1
#     return output

def parse_n_release(i):
    try:
        return re.search(r'[0-9,]+', i).group(0)
    except:
        return ''

def parse_artist(a_tags):
    output = []
    if len(a_tags) > 1:
        for a_tag in a_tags:
            html = bs4.BeautifulSoup(a_tag, 'html.parser')
            _dict = {
                "name": html.get_text(),
                "href": html.find('a')['href']
                }
            output.append(_dict)
    elif len(a_tags) == 1:
        html = bs4.BeautifulSoup(a_tags[0], 'html.parser')
        _dict = {
            "name": html.get_text(),
            "href": html.find('a')['href']
            }
        output.append(_dict)
    return output

class rateYourMusicItem(scrapy.Item):
    """
    Fields used to join collections:
        genre: Key for `genre_metadata` and `genre_hierarchy` collections
        release_id: Key for `release_metadata` and `release_review` 
    """
    # Genre-Level
    # -- Metadata
    genre = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    n_release = scrapy.Field(input_processor=MapCompose(parse_n_release), output_processor=Join(''))
    genre_description = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=Join(' '))
    top_level = scrapy.Field(output_processor=TakeFirst())
    related_descriptors = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=Join(', '))
    
    # -- Hierarchy
    hierarchy = scrapy.Field(input_processor=MapCompose(parse_hierarchy))
    hierarchy_structure = scrapy.Field(output_processor=TakeFirst())
    
    # Sub-Genre_Level Metadata
    # genre = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # n_release = scrapy.Field(input_processor=MapCompose(parse_n_release), output_processor=Join(''))
    # genre_description = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=Join(' '))
    # top_level = scrapy.Field(output_processor=TakeFirst())
    # related_descriptors = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=Join(', '))
    
    # Release-Level
    # -- Metadata
    release_id = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    release_name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    artists = scrapy.Field(input_processor=Compose(parse_artist))
    release_type = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    release_date = scrapy.Field(output_processor=Join(''))
    rating = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst()) # Max rating = 5.0
    n_ratings = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    rank = scrapy.Field(output_processor=Join(''))
    primary_genres = scrapy.Field()
    secondary_genres = scrapy.Field()
    descriptors = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=Join(', '))
    language = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    
    # -- Review
    # release_id = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    review_user = scrapy.Field()
    review_date = scrapy.Field()
    rating_score = scrapy.Field()
    review_content = scrapy.Field()
    rating_id = scrapy.Field()
    
    # Housekeeping fields
    response_url = scrapy.Field(output_processor=TakeFirst())
    spider = scrapy.Field(output_processor=TakeFirst())
    crawl_date = scrapy.Field(output_processor=TakeFirst())