import scrapy
import re
from itemloaders.processors import MapCompose, Join, TakeFirst, Compose

def extract_cast_id(item):
    regex = re.compile(r"/name/(.+)/")
    if regex.match(item):
        return regex.match(item).group(1)
    else:
        return item

class ImdbProfessionalItem(scrapy.Item):
    # Key fields
    # -- get_cast_id.py, imdb_role.py
    cast_id = scrapy.Field(input_processor=MapCompose(extract_cast_id), output_processor=TakeFirst())

    # -- imdb_award.py
    cast_name = scrapy.Field(output_processor=TakeFirst())
    awarding_entity = scrapy.Field(output_processor=TakeFirst())
    award_year = scrapy.Field(output_processor=TakeFirst())
    award_url = scrapy.Field(output_processor=TakeFirst())
    award_outcome = scrapy.Field(output_processor=TakeFirst())
    award_category = scrapy.Field(output_processor=TakeFirst())
    award_title = scrapy.Field(output_processor=TakeFirst())
    movie_detail = scrapy.Field()

    # Housekeeping fields
    scrape_url = scrapy.Field(output_processor = TakeFirst())
    spider = scrapy.Field(output_processor = TakeFirst())
    scrape_date = scrapy.Field(output_processor = TakeFirst())

