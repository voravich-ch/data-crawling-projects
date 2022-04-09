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

# Load credentials
load_dotenv()

def main():
    # Initialise spotifyCrawler
    crawler = spotifyCrawler(_id=os.environ.get('_id'), _secret=os.environ.get('_secret'))
    
    # Artist-level data
    collection = connect_to_db(db_name='spotify', collection_name='artist_id')
    artist_ids = [i['artist_id'] for i in collection.find({}, projection = {"_id": 0, "artist_id": 1})]
    for chunk in tqdm(batch(artist_ids, 50)):
        document = crawler.request_artists_meta(chunk)
        insert_data_to_mongo(data=document, collection=connect_to_db(db_name='spotify', collection_name='test_artist'))
    
    # Album-level data
    for artist_id in tqdm(artist_ids):
        document = crawler.request_albums_from_artist(artist_id)
        insert_data_to_mongo(data=document, collection=connect_to_db(db_name='spotify', collection_name='test_album'))
    
    # Track-level data
    collection = connect_to_db(db_name='spotify', collection_name='test_album')
    album_ids = [i['id'] for i in collection.find({}, projection = {"_id": 0, "id": 1})]
    for album_id in tqdm(album_ids):
        document = crawler.request_tracks_from_album(album_id)
        insert_data_to_mongo(data=document, collection=connect_to_db(db_name='spotify', collection_name='test_track'))
    
    # Acoustic attributes
    collection = connect_to_db(db_name='spotify', collection_name='test_track')
    track_ids = [i['id'] for i in collection.find({}, projection = {"_id": 0, "id": 1})]
    for chunk in tqdm(batch(track_ids, 100)):
        document = crawler.request_acoustic_attributes(track_ids)
        insert_data_to_mongo(data=document, collection=connect_to_db(db_name='spotify', collection_name='test_acoustic_attributes'))
    
if __name__ == "__main__":
    main()