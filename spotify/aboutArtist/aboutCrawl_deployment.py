#!/usr/bin/env python3
# -*- encoding utf-8 -*-

"""
This script utilises Spotify Artist ID to crawl the 'About' section on Spotify artist page:
Fields:
    - followers: (str), Number of followers
    - monthly_listeners: (str), Number of monthly listeners
    - monthly_listeners_by_country: (list of dictionary (keys: "country", "listeners")), Number of monthly listeners by country
    - about: (dictionary (keys: "text", "hrefs")), About section with hrefs of those (i.e., other artists) mentioned in the text
"""

from aboutCrawl import spotifyAboutCrawler, get_urls_from_grammy
from tqdm import tqdm
import datetime
import time

def main():
    # Initialise spotifyAboutCrawler
    crawler = spotifyAboutCrawler()
    
    # Start Selenium session
    crawler.start_session()
    
    # Get spotify urls from grammyAwards database
    spotify_urls = get_urls_from_grammy(db_name='grammyAwards', collection_name='artists_googleSearch')
    
    # Start crawling
    # Use while loop to recollect unsuccessful requests
    while spotify_urls:
        for url in tqdm(spotify_urls):
            try:
                crawler.process_web(url)
                time.sleep(1)
                record = {
                    "name": crawler.get_name(),
                    "rank": crawler.get_rank(),
                    "followers" : crawler.get_followers(),
                    "monthly_listeners": crawler.get_monthly_listeners(),
                    "monthly_listeners_by_country": crawler.get_monthly_listeners_by_country(),
                    "about": crawler.get_about(),
                    "response_url": url,
                    "crawl_date": datetime.datetime.now().strftime('%d/%m/%Y')
                }
                # Store data in local storage
                crawler.write_data_to_local(data=record, f_name='aboutArtist.jl')
                
                # Store data in MongoDB
                crawler.insert_data_to_mongo(data=record, db_name='grammyAwards', collection_name='spotify_about')
                
                # Remove successful url
                spotify_urls.remove(url)
            except:
                print(f'Re-visit page: {url}')
    # Close Selenium session
    crawler.end_session()

if __name__ == '__main__':
    main()
