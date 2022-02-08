import scrapy
import re
from datetime import datetime
from itemloaders.processors import MapCompose, Join, TakeFirst, Compose
from w3lib.html import remove_tags
from urllib.parse import urljoin

def clean_number(value):
    value = value.replace(',', '')
    number = re.search(r'[\d]+', value).group(0) 
    return number

def parse_desc(item):
    # get the longest text
    item = [remove_tags(i) for i in item]
    n_word = [len(i.strip().split()) for i in item]
    longest_i = n_word.index(max(n_word))
    final_item = item[longest_i].strip()
    return final_item

def parse_genre(item):
    # get the first element
    item = [remove_tags(i) for i in item]
    item = item[0].replace(' ', '').strip()
    item = item.split(',')
    return item

def extract_score_dist(items):
    # clean items
    items = [remove_tags(i).replace(',', '') for i in items]
    num = [re.search(r'[\d]+', i).group(0) for i in items]
    return num

def parse_cr(item):
    item = [remove_tags(i) for i in item]
    # critic publication name is stored in two different ways -- one of the elements will be empty
    # filter the empty field out
    # format = list(publication, critic_name)
    item = list(filter(str.strip, item))
    return item

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

class metacriticItem(scrapy.Item):
    # key
    mt_tconst = scrapy.Field(output_processor = TakeFirst())
    
    # url field
    mt_url = scrapy.Field(input_processor = MapCompose(lambda i: urljoin('https://www.metacritic.com', i)), output_processor = TakeFirst())
    
    # movie_info fields
    mt_movie_name = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    mt_genre = scrapy.Field(input_processor = Compose(parse_genre))
    mt_movie_desc = scrapy.Field(input_processor = Compose(parse_desc), output_processor = TakeFirst())
    mt_distributor = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    mt_release_date = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    mt_user_n_review = scrapy.Field(input_processor = MapCompose(remove_tags, clean_number, int), output_processor = TakeFirst())
    mt_cr_n_review = scrapy.Field(input_processor = MapCompose(remove_tags, clean_number, int), output_processor = TakeFirst())
    
    # score fields
    mt_cr_score = scrapy.Field(input_processor = MapCompose(remove_tags, int), output_processor = TakeFirst())
    mt_user_score = scrapy.Field(input_processor = MapCompose(remove_tags, lambda i: float(i) if i.isnumeric() else i),
                                 output_processor = TakeFirst())
    mt_cr_n_score = scrapy.Field(input_processor = MapCompose(remove_tags, clean_number, int), output_processor = TakeFirst())
    mt_user_n_score = scrapy.Field(input_processor = MapCompose(remove_tags, clean_number, int), output_processor = TakeFirst())
    mt_user_n_pos = scrapy.Field(input_processor = Compose(lambda i: extract_score_dist(i)[0], int), output_processor = TakeFirst())
    mt_user_n_neg = scrapy.Field(input_processor = Compose(lambda i: extract_score_dist(i)[2], int), output_processor = TakeFirst())
    mt_user_n_mixed = scrapy.Field(input_processor = Compose(lambda i: extract_score_dist(i)[1], int), output_processor = TakeFirst())
    mt_cr_n_pos = scrapy.Field(input_processor = Compose(lambda i: extract_score_dist(i)[0], int), output_processor = TakeFirst())
    mt_cr_n_neg = scrapy.Field(input_processor = Compose(lambda i: extract_score_dist(i)[2], int), output_processor = TakeFirst())
    mt_cr_n_mixed = scrapy.Field(input_processor = Compose(lambda i: extract_score_dist(i)[1], int), output_processor = TakeFirst())
    
    # review fields
    mt_user = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    mt_user_review_score = scrapy.Field(input_processor = MapCompose(remove_tags, int), output_processor = TakeFirst())
    mt_user_review_date = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    mt_user_review = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    mt_user_review_full_url = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    mt_user_review_full = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = Join(' '))
    
    mt_cr = scrapy.Field(input_processor = Compose(parse_cr))
    mt_cr_review_score = scrapy.Field(input_processor = MapCompose(remove_tags, int), output_processor = TakeFirst())
    mt_cr_review_date = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    mt_cr_review = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    mt_cr_review_full_url = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    mt_cr_review_full = scrapy.Field(input_processor = MapCompose(clean_content), output_processor = Join(' '))
    mt_cr_review_full_all = scrapy.Field(input_processor = MapCompose(remove_tags, clean_content), output_processor = Join(' '))
    
    # director_cast fields
    mt_director = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip))
    mt_cast = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip))
    
    # housekeeping fields
    url = scrapy.Field(output_processor = TakeFirst())
    spider = scrapy.Field(output_processor = TakeFirst())
    date = scrapy.Field(output_processor = TakeFirst())