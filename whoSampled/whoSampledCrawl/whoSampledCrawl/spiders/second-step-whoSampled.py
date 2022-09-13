# As mentioned in whoSampled.py;
# If a song contains samples or was sampled by more than 3 songs, 
# a visit to href: /samples or /sampled is necessary to collect all the connections.
# There are 16 items per page; hence, we can parse the navigation instead of doing pagination (more efficient)
# This script will perform the above process

import scrapy
from whoSampledCrawl.items import whoSampledCrawlItem
from scrapy.loader import ItemLoader
import datetime
import pymongo
import pandas as pd

def get_data():
    client = pymongo.MongoClient()
    db = client['whoSampled']
    collection = db['whoSampled']
    df = pd.DataFrame(collection.find({}, projection = {"_id": 0}))
    return df

def prepare_urls(df):
    # Subset df to better see the data
    df = df[['response_url', 'n_sample', 'n_sampled']]
    # Replace nan with 0
    df = df.fillna(0)
    # Convert to int
    df['n_sample'] = df['n_sample'].astype(int)
    df['n_sampled'] = df['n_sampled'].astype(int)
    # Select only those with n_sample >= 4 or n_sampled >= 4
    df = df[(df['n_sample']>=4) | (df['n_sampled']>=4)]
    # Add page number columns
    df['pg_sample'] = df['n_sample'] // 16 + 1
    df['pg_sampled'] = df['n_sampled'] // 16 + 1
    # Initialise a list to store urls
    urls = []
    for idx, row in df.iterrows():
        if row['n_sample'] >=4:
            to_extend = [f"{row['response_url']}samples/?cp={i}" for i in range(1, row['pg_sample']+1)]
            urls.extend(to_extend)
        if row['n_sampled'] >=4:
            to_extend = [f"{row['response_url']}sampled/?cp={i}" for i in range(1, row['pg_sampled']+1)]
            urls.extend(to_extend)
    return urls

# Parameter preparation
df = get_data()
urls = prepare_urls(df)

# Setting up XPath
samples_xpath = '//span[contains(text(), "Contains samples of")]/ancestor::section/div/div'
sampled_xpath = '//span[contains(text(), "Was sampled in")]/ancestor::section/div/div'

class secondStepWhoSampledSpider(scrapy.Spider):
    name = 'second-step-whoSampled'
    allowed_domains = ['whosampled.com']
    start_urls = urls
    
    def parse(self, response):
        # Create itemloader
        l = ItemLoader(item=whoSampledCrawlItem(), response=response)
        
        # Primary fields
        l.add_xpath('samples', samples_xpath)
        l.add_xpath('sampled', sampled_xpath)
        
        # Housekeeping fields
        l.add_value('response_url', response.url)
        l.add_value('spider', self.name)
        l.add_value('crawl_date', datetime.datetime.now().strftime('%d/%m/%Y'))
        
        return l.load_item()
