import scrapy
import re
from datetime import datetime
from itemloaders.processors import MapCompose, Join, TakeFirst, Compose
from w3lib.html import remove_tags
from urllib.parse import urljoin

# def parse_release_date(date):
#     # raw data: e.g. 'Jul 30, 2019'
#     # parse date
#     date = [remove_tags(i) for i in date]
#     date = [i.strip() for i in date]
#     date = [datetime.strptime(i, '%b %d, %Y') for i in date]
#     date = [i.strftime('%d/%m/%Y') for i in date]
#     return date

def parse_desc(item):
    # get the longest text
    item = [remove_tags(i) for i in item]
    n_word = [len(i.strip().split()) for i in item]
    longest_i = n_word.index(max(n_word))
    final_item = item[longest_i].strip()
    return final_item

def parse_list(item):
    try:
        item = [remove_tags(i) for i in item]
        item = re.sub(r'[\n ]', '', item[0])
        item = item.split(',')
        return item
    except:
        None

def clean_content(item):
    # set minimum of words in a string to consider a paragraph
    min_word = 10
    # remove tags
    item = remove_tags(item).strip()
    n_word = len(item.split())
    if n_word > min_word: 
        content = item
    else: 
        content = None
    return content

class rottenTomatoesItem(scrapy.Item):
    # key
    rt_tconst = scrapy.Field(output_processor = TakeFirst())
    
    # url field
    rt_url = scrapy.Field(output_processor = TakeFirst())
    
    # movie_info fields
    rt_title = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    rt_user_rating = scrapy.Field(input_processor = MapCompose(remove_tags, lambda i: int(i) if i.isnumeric() else i),
                                  output_processor = TakeFirst())
    rt_cr_rating = scrapy.Field(input_processor = MapCompose(remove_tags, lambda i: int(i) if i.isnumeric() else i),
                                output_processor = TakeFirst())
    rt_movie_desc = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    rt_genre = scrapy.Field(input_processor = Compose(parse_list))
    rt_director = scrapy.Field(input_processor = Compose(parse_list))
    rt_producer = scrapy.Field(input_processor = Compose(parse_list))
    rt_writer = scrapy.Field(input_processor = Compose(parse_list))
    rt_release_date_th = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    rt_release_date_st = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    rt_gross_us = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    rt_production = scrapy.Field(input_processor = Compose(parse_list))
    
    # # user_review fields
    # user = scrapy.Field(input_processor = MapCompose(remove_tags))
    # topic = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip))
    # user_content = scrapy.Field(input_processor = MapCompose(remove_tags))
    # review_date = scrapy.Field()
    # user_rating = scrapy.Field()
    # n_helpful_vote = scrapy.Field(
    #     input_processor = MapCompose(remove_tags, lambda i: re.findall(r'([\d]+)', i.replace(',', ''))[0], int))
    # total_helpful_vote = scrapy.Field(
    #     input_processor = MapCompose(remove_tags, lambda i: re.findall(r'([\d]+)', i.replace(',', ''))[1], int))
    
    # critic_review fields
    rt_cr = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    rt_pub = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    rt_top = scrapy.Field(input_processor = MapCompose(lambda i: 1), output_processor = TakeFirst())
    rt_fresh = scrapy.Field(input_processor = MapCompose(lambda i: 1), output_processor = TakeFirst())
    rt_cr_review = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    rt_cr_review_full = scrapy.Field(input_processor = MapCompose(clean_content), output_processor = Join(' '))
    rt_cr_review_full_all = scrapy.Field(input_processor = MapCompose(clean_content), output_processor = Join(' '))
    rt_cr_review_full_url = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    rt_cr_review_date = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    
    # housekeeping fields
    url = scrapy.Field(output_processor = TakeFirst())
    spider = scrapy.Field(output_processor = TakeFirst())
    date = scrapy.Field(output_processor = TakeFirst())