import pymongo
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials as credentials
import os
import re
import json
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

def connect_to_spotify():
    load_dotenv()
    _id = os.environ.get('_id')
    _secret = os.environ.get('_secret')
    spotify = sp.Spotify(auth_manager=credentials(client_id=_id, client_secret=_secret))
    return spotify

def connect_to_city(db_name, collection_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    return collection

def get_id(collection):
    cursor = collection.find({}, projection = {"_id": 0, "variables": 1, "request_url": 1})
    # Get document while remove duplicates (Obsolete track ids)
    trackInfo = [document['variables']['track'] for document in cursor if document['variables']['track']['id'] == int(re.search(r'\d+', document['request_url']).group(0))]
    tracks = [{'musixmatchId': track['id'], 'spotifyId': track['spotifyId']} for track in trackInfo if track['spotifyId']]
    return tracks

class spotifyCrawler:
    """
    Crawl data from spotify
    
    Parameters
    ----------
    tracks : list of dictionaries with keys: 'musixmatchId' and 'spotifyId'
        Example: [
            {'musixmatchId': 6556144, 'spotifyId': '07Kzz3FP2o5rigf0HB2B1b'}, 
            {'musixmatchId': 6556146, 'spotifyId': '7IfgtOu545iMfVKNLyUBr3'},
            ]
    client : Spotify client
        For reference, see: https://spotipy.readthedocs.io/en/2.19.0/#module-spotipy.client
    collection : PyMongo collection
        For reference, see: https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-collection
    """
    
    def __init__(self, tracks, client, collection):
        self.tracks = tracks
        self.client = client
        self.collection = collection
    
    def start_crawling(self):
        assert isinstance(self.tracks, list), 'Please ensure that the `tracks` parameter is a list.'
        assert self.tracks != [], '`tracks` parameter is an empty list.'
        assert list(pd.DataFrame(self.tracks).columns) == ['musixmatchId', 'spotifyId'], '`track` parameter is not in a correct format.'
        
        n_tracks = len(self.tracks)
        max_capacity = 100
        # Case when the number of tracks is below the maximum capacity (100)
        if n_tracks <= max_capacity:
            self.batch = pd.DataFrame(self.tracks)
            self.process_request()
            print(f'Data is stored at: {self.collection.full_name}')
        # Case when the number of tracks is over the maximum capacity (100)
        elif n_tracks > max_capacity:
            batch_size = max_capacity
            n_batch = n_tracks // batch_size
            for i in range(n_batch):
                self.batch = pd.DataFrame(self.tracks[i*batch_size:(i+1)*batch_size])
                self.process_request()
            # If there are remaining tracks
            if n_tracks % batch_size != 0:
                # Process remaining tracks
                self.batch = pd.DataFrame(self.tracks[n_batch*batch_size:])
                self.process_request()
            print(f'Data is stored at: {self.collection.full_name}')
    
    def process_request(self):
        # Request acoustic attributes
        song = self.spotifyAcoustic(tracks=self.batch, client=self.client)
        # Parse data
        documents = song.parse_data()
        # Insert documents to the MongoDB collection
        self.collection.insert_many(documents)
    
    class spotifyAcoustic:
        def __init__(self, tracks, client):
            self.tracks = tracks
            self.client = client
            
        def parse_data(self):
            # Request acoustic attributes
            self.data = self.client.audio_features(self.tracks['spotifyId'])
            # Remove null values: Some ids do not exist anymore
            self.data = pd.DataFrame(filter(None, self.data))
            # Append musixmatchId
            self.data = pd.merge(self.data, self.tracks, how='left', left_on='id', right_on='spotifyId').drop(columns='spotifyId')
            # Prepare data to insert to MongoDB
            self.data = self.data.to_dict('records')
            return self.data

def main():
    # Connect to Spotify
    spotify = connect_to_spotify()
    # Connect to musixmatch database
    collection = connect_to_city(db_name='musixmatch', collection_name='sample')
    tracks = get_id(collection) # List of dict with keys: 'musixmatchId' and 'spotifyId'
    # Connect to spotify database
    collection = connect_to_city(db_name='spotify', collection_name='acousticAttributesSample')
    # Initialise crawler
    crawler = spotifyCrawler(tracks=tracks, client=spotify, collection=collection)
    # Start crawling
    crawler.start_crawling()
    
if __name__ == "__main__":
    main()