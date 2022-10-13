#!/usr/bin/env python3
# -*- encoding utf-8 -*-

"""
This script utilises Spotify Artist ID to crawl the following data from Spotify:
    - Artist Level Data
    - Album Level Data
    - Track Level Data
    - Acoustic Attributes (Audio Features)
"""

from spotifyCrawl import *
from dotenv import load_dotenv
from tqdm import tqdm
import random
import time

# Load credentials
load_dotenv()

def main():
    # Initialise spotifyCrawlers
    crawler = spotifyCrawler(_id=os.environ.get('_id'), _secret=os.environ.get('_secret'))
    
    # Artist-level data
    collection = connect_to_db(db_name='spotify', collection_name='artist_id')
    artist_ids = [i['artist_id'] for i in collection.find({}, projection = {"_id": 0, "artist_id": 1}).skip(0).limit(0)]
    for chunk in tqdm(batch(artist_ids, 50)):
        document = crawler.request_artists_meta(chunk)
        insert_data_to_mongo(data=document, collection=connect_to_db(db_name='spotify', collection_name='artists'))
        time.sleep(random.randint(0, 3))
    print("Artist-level data completed.")
    
    # Album-level data
    for artist_id in tqdm(artist_ids):
        document = crawler.request_albums_from_artist(artist_id)
        insert_data_to_mongo(data=document, collection=connect_to_db(db_name='spotify', collection_name='albums'))
        time.sleep(random.randint(0, 3))
    print("Album-level data completed.")
    
    # Track-level data
    collection = connect_to_db(db_name='spotify', collection_name='test_album')
    album_ids = [i['id'] for i in collection.find({}, projection = {"_id": 0, "id": 1}).skip(0).limit(0)]
    for album_id in tqdm(album_ids):
        document = crawler.request_tracks_from_album(album_id)
        insert_data_to_mongo(data=document, collection=connect_to_db(db_name='spotify', collection_name='tracks'))
        time.sleep(random.randint(0, 3))
    print("Track-level data completed.")
    
    # Acoustic attributes
    collection = connect_to_db(db_name='spotify', collection_name='test_track')
    track_ids = [i['id'] for i in collection.find({}, projection = {"_id": 0, "id": 1}).skip(0).limit(0)]
    for chunk in tqdm(batch(track_ids, 100)):
        document = crawler.request_acoustic_attributes(chunk)
        # Filter None
        document = list(filter(lambda item: item is not None, document))
        insert_data_to_mongo(data=document, collection=connect_to_db(db_name='spotify', collection_name='acousticAttributes'))
        time.sleep(random.randint(0, 3))
    print("Acoustic attributes data completed.")
    
if __name__ == "__main__":
    main()
