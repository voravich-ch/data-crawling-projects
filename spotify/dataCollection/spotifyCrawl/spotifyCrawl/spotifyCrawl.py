import pymongo
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials as credentials
import os
import re
import json
import pandas as pd
from tqdm import tqdm

class spotifyCrawler:
    
    def __init__(self, _id, _secret):
        self._id = _id
        self._secret = _secret
        self.spotify = sp.Spotify(auth_manager=credentials(client_id=_id, client_secret=_secret))
        
    def request_artists_meta(self, artist_ids):
        """
        Request artist meta data from artist ids
        """
        return self.spotify.artists(artist_ids)
    
    def request_albums_from_artist(self, artist_id):
        """
        Request up to 50 albums from an artist id
        """
        return self.spotify.artist_albums(artist_id, limit=50)['items']
    
    def request_tracks_from_album(self, album_id):
        """
        Request up to 50 tracks from an album id
        """
        return self.spotify.album_tracks(album_id, limit=50)['items']
    
    def request_acoustic_attributes(self, track_ids):
        """
        Request acoustic attributes from up to 100 track ids
        """
        return self.spotify.audio_features(track_ids)

def connect_to_db(db_name, collection_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    return collection

def insert_data_to_mongo(data, collection):
    collection.insert_many(pd.DataFrame(data).to_dict('records'))

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]