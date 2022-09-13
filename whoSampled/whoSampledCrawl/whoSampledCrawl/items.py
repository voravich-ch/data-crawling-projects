import scrapy
from itemloaders.processors import MapCompose, Compose, Join, TakeFirst
import re
import bs4
from urllib.parse import urljoin

def parse_a_tags(a_tags):
    output = []
    for a_tag in a_tags:
        html = bs4.BeautifulSoup(a_tag, 'html.parser')
        _dict = {
            "text": html.get_text(),
            "link": urljoin('https://www.whosampled.com', html.find('a')['href'])
        }
        output.append(_dict)
    return output

def parse_artists_raw_text(l):
    l = list(map(str.strip, l))
    l = list(filter(None, l))
    return l

def parse_sample(l):
    output = []
    extract_year = re.compile(r'\((\d+)\)')
    for item in l:
        html = bs4.BeautifulSoup(item, 'html.parser')
        _dict = {
            "track_name": html.select_one('a[class*="trackName"]').get_text(),
            "track_link": urljoin('https://www.whosampled.com', html.select_one('span[class*="trackArtist"] a')['href']) + html.select_one('a[class*="trackName"]').get_text().replace(' ', '-'),
            "track_sample_link": urljoin('https://www.whosampled.com', html.select_one('a[class*="trackName"]')['href']),
            "main_artist_name": html.select_one('span[class*="trackArtist"] a').get_text(),
            "main_artist_link": urljoin('https://www.whosampled.com', html.select_one('span[class*="trackArtist"] a')['href']),
            "artists": parse_a_tags(list(map(str, html.select('span[class*="trackArtist"] a')))),
            "year": extract_year.search(html.select_one('span[class*="trackArtist"]').get_text()).group(1),
            "sample_element": html.select_one('div[class="trackBadge"] span[class="topItem"]').get_text(),
            "track_genre": html.select_one('div[class="trackBadge"] span[class="bottomItem"]').get_text()
        }
        output.append(_dict)
    return output

class whoSampledCrawlItem(scrapy.Item):
    # Primary fields
    song_name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    artists = scrapy.Field(input_processor=Compose(parse_a_tags))
    artists_raw_text = scrapy.Field(input_processor=Compose(parse_artists_raw_text), output_processor=Join(' '))
    album_name = scrapy.Field(input_processor=Compose(parse_a_tags), output_processor=TakeFirst())
    release_year = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    producers = scrapy.Field(input_processor=Compose(parse_a_tags))
    genre = scrapy.Field(input_processor=Compose(parse_a_tags), output_processor=TakeFirst())
    tags = scrapy.Field(input_processor=Compose(parse_a_tags))
    n_sample = scrapy.Field(input_processor=MapCompose(lambda i: re.search(r'\d+', i).group(0)), output_processor=TakeFirst())
    n_sampled = scrapy.Field(input_processor=MapCompose(lambda i: re.search(r'\d+', i).group(0)), output_processor=TakeFirst())
    samples = scrapy.Field(input_processor=Compose(parse_sample))
    sampled = scrapy.Field(input_processor=Compose(parse_sample))
    
    # Housekeeping fields
    response_url = scrapy.Field(output_processor=TakeFirst())
    spider = scrapy.Field(output_processor=TakeFirst())
    crawl_date = scrapy.Field(output_processor=TakeFirst())
