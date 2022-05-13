import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from beerAdvocateCrawl.items import beerAdvocateCrawlItem
from scrapy.loader import ItemLoader
import os
import re
import datetime
import requests
import bs4
from urllib.parse import urljoin

def get_forum_urls():
    # Get forum URLs from the Community page
    base_url = 'https://www.beeradvocate.com/community/'
    response = requests.get(base_url)
    html = bs4.BeautifulSoup(response.text, 'html.parser')
    a_tags = html.find_all('a', href=True)
    urls = [urljoin(base_url, a_tag['href']) for a_tag in a_tags if re.search(r'^forums/.+', a_tag['href'])]
    return urls

# Parameters preparation
urls = get_forum_urls()

# XPath
posts_xpath = '//li[contains(@id, "post-")]'

# -- Forum housekeeping
forum_xpath = '//p[@id="pageDescription"]/a[contains(@href, "forums")]'
thread_url_xpath = '//meta[@property="og:url"]/@content'
thread_topic_xpath = '//h1/text()'
thread_starter_xpath = '//p[@id="pageDescription"]/a[contains(@href, "members")]'
thread_start_date_xpath = '//p[@id="pageDescription"]/a/abbr/@data-datestring | //p[@id="pageDescription"]/a/span[@class="DateTime"]/text()'

# -- Content
author_xpath = './/a[@class="username author"]'
comment_xpath = './/blockquote/text()'
comment_id_xpath = './@id'
comment_date_xpath = './/span[@class="DateTime"]/text()'
comment_order_xpath = './/a[contains(@class, "postNumber")]/text()'
quotes_xpath = './/div[@class="bbCodeBlock bbCodeQuote"]/aside'
n_likes_xpath = './/div[contains(@class, "likesSummary")]/span[@class="LikeText"]'


class forumSpider(CrawlSpider):
    name = 'forum'
    allowed_domains = ['beeradvocate.com']
    start_urls = urls
    
    # Rules for horizontal / vertical crawling
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[contains(text(), "Next")]')),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="PreviewTooltip"]'), callback='parse')
    )
    
    def parse(self, response):
        # List of posts
        posts = response.xpath(posts_xpath)
        
        for post in posts:
            # Create loader
            l = ItemLoader(item=beerAdvocateCrawlItem(), selector=post)
            
            # Forum housekeeping fields
            l.add_xpath('forum', forum_xpath)
            l.add_xpath('thread_url', thread_url_xpath)
            l.add_xpath('thread_topic', thread_topic_xpath)
            l.add_xpath('thread_starter', thread_starter_xpath)
            l.add_xpath('thread_start_date', thread_start_date_xpath)
            
            # Content fields
            l.add_xpath('author', author_xpath)
            l.add_xpath('comment', comment_xpath)
            l.add_xpath('comment_id', comment_id_xpath)
            l.add_xpath('comment_date', comment_date_xpath)
            l.add_xpath('comment_order', comment_order_xpath)
            l.add_xpath('quotes', quotes_xpath)
            l.add_xpath('n_likes', n_likes_xpath)
            
            # Housekeeping fields
            l.add_value('response_url', response.url)
            l.add_value('spider', self.name)
            l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
            
            yield l.load_item()