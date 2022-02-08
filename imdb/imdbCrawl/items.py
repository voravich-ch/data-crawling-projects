import scrapy
import re
from datetime import datetime
from itemloaders.processors import MapCompose, Join, TakeFirst
from w3lib.html import remove_tags

def clean_number(value):
    value = value.replace(',', '')
    number = re.search(r'[\d]+', value).group(0) 
    return number

def clean_content(item):
    # set minimum of words in a string to consider a paragraph
    min_word = 10
    n_word = len(item.strip().split())
    if n_word > min_word: 
        content = item.strip()
    else: 
        content = None
    return content

def parse_n_rating(item):
    item = re.search(r'\"ratingCount.+?(?=(\d+))', item)
    if item:
        return item.group(1)
    else:
        return None

class imdbItem(scrapy.Item):
    # key
    imdb_tconst = scrapy.Field(output_processor = TakeFirst())
    
    # movie_desc fields
    imdb_title = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    imdb_rating = scrapy.Field(input_processor = MapCompose(remove_tags, lambda i: re.search(r'[.0-9]+', i).group(0), float),
                               output_processor = TakeFirst())
    imdb_n_rating = scrapy.Field(input_processor = MapCompose(remove_tags, parse_n_rating, int), output_processor = TakeFirst())
    imdb_movie_desc = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = Join())
    imdb_user_n_review = scrapy.Field(input_processor = MapCompose(remove_tags, clean_number, int),
                                      output_processor = TakeFirst())
    imdb_cr_n_review = scrapy.Field(input_processor = MapCompose(remove_tags, clean_number, int),
                                    output_processor = TakeFirst())
    imdb_budget = scrapy.Field(input_processor = MapCompose(remove_tags, clean_number, int),
                               output_processor = TakeFirst())
    imdb_gross_us = scrapy.Field(input_processor = MapCompose(remove_tags, clean_number, int),
                                 output_processor = TakeFirst())
    imdb_sequel = scrapy.Field()
    imdb_distributor = scrapy.Field()
    imdb_release_date = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    
    # user_review fields
    imdb_user = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    imdb_user_review_topic = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    imdb_user_review = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    imdb_user_review_date = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    imdb_user_rating = scrapy.Field(input_processor = MapCompose(remove_tags, int), output_processor = TakeFirst())
    imdb_n_helpful_vote = scrapy.Field(
        input_processor = MapCompose(remove_tags, lambda i: re.findall(r'([\d]+)', i.replace(',', ''))[0], int),
        output_processor = TakeFirst())
    imdb_t_vote = scrapy.Field(
        input_processor = MapCompose(remove_tags, lambda i: re.findall(r'([\d]+)', i.replace(',', ''))[1], int),
        output_processor = TakeFirst())
    
    # critic_review fields
    imdb_cr = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    imdb_cr_url = scrapy.Field(output_processor = TakeFirst())
    imdb_cr_review = scrapy.Field(input_processor = MapCompose(clean_content), output_processor = Join(' '))
    imdb_cr_review_all = scrapy.Field(input_processor = MapCompose(remove_tags, clean_content), output_processor = Join(' '))
    
    # director_cast fields
    imdb_director = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip))
    imdb_cast = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip))
    
    # metacritic_link fields
    imdb_mt_url = scrapy.Field(
        input_processor = MapCompose(lambda i: re.match(r'^(.*?)\?', i).group(1)),
        output_processor = TakeFirst())
    
    # housekeeping fields
    url = scrapy.Field(output_processor = TakeFirst())
    spider = scrapy.Field(output_processor = TakeFirst())
    date = scrapy.Field(output_processor = TakeFirst())