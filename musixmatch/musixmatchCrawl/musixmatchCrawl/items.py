# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import json
from itemloaders.processors import MapCompose, Join, TakeFirst
from w3lib.html import remove_tags

def variables_to_json(item):
    """
    The input contains a html script with variables structured in json format.
    The necessary information is extracted via regular expression and format as json. 
    """
    # Extract everything after `var __mxmState` not including ';' at the end
    pattern = r'mxmState = (.+)(;)'
    _var = re.search(pattern, item)[1]
    # Format as json
    _json = json.loads(_var)
    # Extract values from the key: 'page'
    output = _json['page']
    return output
    
class musixmatchItem(scrapy.Item):
    # Primary fields
    variables = scrapy.Field(input_processor=MapCompose(variables_to_json), output_processor=TakeFirst())
    lyric = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Join())
    
    # Housekeeping fields
    request_url = scrapy.Field(output_processor=TakeFirst())
    response_url = scrapy.Field(output_processor=TakeFirst())
    spider = scrapy.Field(output_processor=TakeFirst())
    crawl_date = scrapy.Field(output_processor=TakeFirst())