import scrapy
from imdb_professional.items import ImdbProfessionalItem
from scrapy.loader import ItemLoader

import re
import datetime
import pymongo
from urllib.parse import urljoin

# Parameter preparation
# Get urls
mongo_uri = 'mongodb://127.0.0.1:27018'
client = pymongo.MongoClient(mongo_uri)
collection = client['imdbProfessional']['imdb_cast_id']
cursor = collection.find({}, projection = {"_id": 0, "cast_id": 1})
urls = [f"https://www.imdb.com/name/{cast_id['cast_id']}/awards/" for cast_id in cursor]

# -- XPath
cast_name_xpath = '//h3/a/text()'
main_xpath = '//div[@class="article listo"]//h3'

class ImdbAwardSpider(scrapy.Spider):
    name = 'imdb_award'
    allowed_domains = ['imdb.com']
    start_urls = urls

    def parse(self, response):  
        # List of items
        main = response.xpath(main_xpath)
        for h3 in main[1:]: # Excluding the first element which is the cast name
            table = h3.xpath('./following::table[1]')
            awarding_entity = h3.xpath('./text()').get().strip()
            for tr in table.xpath('.//tr'):
                if tr.xpath('.//td[@class="award_year"]'):
                    try:
                        award_year = tr.xpath('.//td[@class="award_year"]/a/text()').get().strip()
                    except:
                        award_year = ''
                    try:
                        award_url = urljoin(response.url, tr.xpath('.//td[@class="award_year"]/a/@href').get())
                    except:
                        award_url = ''
                if tr.xpath('.//td[@class="award_outcome"]'):
                    try:
                        award_outcome = tr.xpath('.//td[@class="award_outcome"]/b/text()').get().strip()
                    except:
                        award_outcome = ''
                    try:
                        award_category = tr.xpath('.//td[@class="award_outcome"]/span/text()').get().strip()
                    except:
                        award_category = ''
                if tr.xpath('.//td[@class="award_description"]'):
                    try:
                        award_title = tr.xpath('.//td[@class="award_description"]/text()').get().strip()
                    except:
                        award_title = ''
                if tr.xpath('.//td[@class="award_description"]/a'):
                    movie_detail = []
                    for a in tr.xpath('.//td[@class="award_description"]//a[contains(@href, "/title/tt")]'):
                        try:
                            movie_name = a.xpath('./text()').get().strip()
                        except:
                            movie_name = ''
                        try:
                            movie_id =  re.search(r"\/(tt.\d+)[\/]?", a.xpath('./@href').get().strip()).group(1)
                        except:
                            movie_id = ''
                        try:
                            movie_year = re.search(r'\d+', a.xpath('./following::span[1]/text()').get()).group(0)
                        except:
                            movie_year = ''
                        _dict = {
                            'movie_name': movie_name,
                            'movie_id': movie_id,
                            'movie_year': movie_year
                        }
                        movie_detail.append(_dict)
                else:
                    movie_detail = []

                # Create loader
                l = ItemLoader(item=ImdbProfessionalItem(), selector=tr)
                
                # Key
                l.add_value('cast_id', re.search(r"\/(nm\d+)\/", response.url).group(1))
                l.add_xpath('cast_name', cast_name_xpath)
                l.add_value('awarding_entity', awarding_entity)
                l.add_value('award_year', award_year)
                l.add_value('award_url', award_url)
                l.add_value('award_outcome', award_outcome)
                l.add_value('award_category', award_category)
                l.add_value('award_title', award_title)
                l.add_value('movie_detail', movie_detail)

                # housekeeping fields
                l.add_value('scrape_url', response.url)
                l.add_value('spider', self.name)
                l.add_value('scrape_date', datetime.datetime.now().strftime('%d/%m/%Y'))
                
                yield l.load_item()
