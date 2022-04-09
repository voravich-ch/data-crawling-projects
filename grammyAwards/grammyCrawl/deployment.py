#!/usr/bin/env python3
# -*- encoding utf-8 -*-

"""
This script crawls artist data from Grammy.com and store in grammyAwards database (MongoDB)
"""

from artistCrawl import *
from tqdm import tqdm
import datetime

def main():
    # Initialise grammyCrawler
    crawler = grammyCrawler()
    
    # Connect to database
    collection = connect_to_db(db_name='grammyAwards2', collection_name='artists')
    
    # Parse start urls from sitemap
    artist_urls = parse_start_urls()
    artist_urls = artist_urls[299+2553:]
    
    for url in tqdm(artist_urls):
        crawler.process_web(url)
        record = {
            "name": crawler.get_name(),
            "wins" : crawler.get_wins(),
            "nominations": crawler.get_nominations(),
            "awards_and_nominations": crawler.get_awards_and_nominations(),
            "response_url": url,
            "crawl_date": datetime.datetime.now().strftime('%d/%m/%Y')
        }
        insert_data_to_mongo(data=record, collection=collection)

if __name__ == "__main__":
    main()
