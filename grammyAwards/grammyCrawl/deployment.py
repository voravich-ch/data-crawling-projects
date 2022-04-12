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
    
    # Start Selenium session
    crawler.start_session()
    
    # Parse start urls from sitemap
    artist_urls = parse_start_urls()
    
    # Start crawling
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
        # Store data in local storage
        crawler.write_data_to_local(data=record, f_name='grammyArtist.jl')
        
        # Store data in MongoDB
        crawler.insert_data_to_mongo(data=record, db_name='grammyAwards', collection_name='artists')
    
    # Close Selenium session
    crawler.end_session()

if __name__ == "__main__":
    main()
