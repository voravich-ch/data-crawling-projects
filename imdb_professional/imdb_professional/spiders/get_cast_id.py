import scrapy
from imdb_professional.items import ImdbProfessionalItem
from scrapy.loader import ItemLoader

import pymongo

# Parameter preparation
# -- Sample title urls
mongo_uri = 'mongodb://127.0.0.1:27018'
client = pymongo.MongoClient(mongo_uri)
collection = client['imdbProfessional']['sample_title']
cursor = collection.find({}, projection = {"_id": 0, "title_id": 1})
urls = [f"https://www.imdb.com/title/{title['title_id']}/fullcredits" for title in cursor]

# -- XPath
casts_xpath = '//table[@class="cast_list"]//td[not(@class)]'
cast_id_xpath = './a[@href]/@href'

class GetCastIdSpider(scrapy.Spider):
    name = 'get_cast_id'
    allowed_domains = ['imdb.com']
    start_urls = urls

    def parse(self, response):
        # List of items
        main = response.xpath(casts_xpath)
        
        for i in main:
            # Create loader
            l = ItemLoader(item=ImdbProfessionalItem(), selector=i)
            
            # Key
            l.add_xpath('cast_id', cast_id_xpath)
            
            yield l.load_item()
