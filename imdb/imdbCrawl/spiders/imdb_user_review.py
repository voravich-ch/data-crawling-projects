import scrapy
from imdbCrawl.items import imdbItem
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest

import os
import re
import datetime
import pandas as pd

from imdbCrawl.modules import get_parent_dir_path

def get_urls(parent_dir_path):
    # set file path
    folder = 'data'
    in_file = 'sample.json'
    target = os.path.join(parent_dir_path, folder, in_file) 
    # load file
    df = pd.read_json(target, orient='records')
    # get movie id
    ids = df.loc[:, 'tconst'].to_list()
    # get movie url
    urls = [f'https://www.imdb.com/title/{i}/reviews' for i in ids]
    return urls

# parameters preparations
parent_dir_path = get_parent_dir_path()
urls = get_urls(parent_dir_path)

# xpaths
main_xpath = '//div[contains(@class, "lister-item-content")]'
imdb_user_xpath = './/span[contains(@class, "display-name-link")]/a'
imdb_user_review_topic_xpath = './/a[contains(@class, "title")]'
imdb_user_review_xpath = './/div[contains(@class, "text")]'
imdb_user_review_date_xpath = './/span[contains(@class, "review-date")]'
imdb_user_rating_xpath = './/span[contains(@class, "rating-other-user-rating")]/span[not(@class)]'
imdb_n_helpful_vote_xpath = './/div[contains(@class, "actions")]'
imdb_t_vote_xpath = './/div[contains(@class, "actions")]'

class imdbUserReviewSpider(scrapy.Spider):
    name = 'imdb_user_review'
    allowed_domains = ['web']
    start_urls = urls
    
    # Splash authentication
    http_user = 'user'
    http_pass = 'userpass'  
    
    def start_requests(self):
        for url in self.start_urls:
            # lua script
            script = """
            function main(splash)
                assert(splash:go(splash.args.url))
                -- Get dimension of the 'load-more' button
                local get_dimensions = splash:jsfunc([[
                    function () {
                        var rect = document.getElementById('load-more-trigger').getClientRects()[0];
                        return {"x": rect.left, "y": rect.top}
                    }
                ]])
                -- Scroll the page
                local scroll_screen = splash:jsfunc([[
                    function () {
                        window.scrollTo(0,document.body.scrollHeight);
                        return document.body.scrollHeight
                    }
                ]])
                -- Logic: Scroll down to the end, click the button
                -- stop if button not found (catch error with pcall) -> arrive at the last review
                local last_scroll_height = 0
                local scroll_height = scroll_screen()
                while last_scroll_height < scroll_height do
                    last_scroll_height = scroll_height
                    scroll_height = scroll_screen()
                    splash:wait(0.3)
                    if pcall(get_dimensions) then
                        dimensions = get_dimensions()
                        splash:mouse_click(dimensions.x, dimensions.y)
                        splash:wait(2)
                        scroll_height = scroll_screen()
                    else
                    end
                end
                return {
                    splash:html()
                }
            end
            """
            
            # render with Splash                

            yield SplashRequest(url, self.parse,
                                endpoint='execute',
                                args={'lua_source': script,
                                      'timeout': 1800})      

    def parse(self, response): 
        # list of reviews
        main = response.xpath(main_xpath)
        
        for i in main:
            # create the loader
            l = ItemLoader(item = imdbItem(), selector = i)
            
            # key
            l.add_value('imdb_tconst', re.search(r'\/(tt.+)\/', response.url).group(1))
        
            # primary fields
            l.add_xpath('imdb_user', imdb_user_xpath)
            l.add_xpath('imdb_user_review_topic', imdb_user_review_topic_xpath)
            l.add_xpath('imdb_user_review', imdb_user_review_xpath)
            l.add_xpath('imdb_user_review_date', imdb_user_review_date_xpath)
            l.add_xpath('imdb_user_rating', imdb_user_rating_xpath)
            l.add_xpath('imdb_n_helpful_vote', imdb_n_helpful_vote_xpath)
            l.add_xpath('imdb_t_vote', imdb_t_vote_xpath)
            
            # housekeeping fields
            l.add_value('url', response.url)
            l.add_value('spider', self.name)
            l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
            yield l.load_item()

