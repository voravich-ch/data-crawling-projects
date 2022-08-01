import os
import re
import numpy as np
import pandas as pd
import pymongo
import time
import random
from tqdm import tqdm
from bson.objectid import ObjectId

import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials as credentials
from dotenv import load_dotenv

def parse_spotify_id(url):
    pattern = r'spotify.com/artist/(\w+)'
    p = re.compile(pattern)
    return p.search(url).group(1)

def get_artist_ids_from_musicbrainz():
    # Connect to MongoDB
    client = pymongo.MongoClient()
    collection = client['musicbrainz']['artist_urls']
    # Get data
    cursor = collection.find({}, projection = {"_id": 0})
    df = pd.DataFrame(cursor)
    # Extract spotify urls
    df = df.loc[df['url'].str.contains('open.spotify.com/artist')]
    # Parse spotify id
    df['artist_id'] = df['url'].apply(parse_spotify_id)
    df = df[['artist_id']]
    # Remove duplicates
    df = df.drop_duplicates()
    return df

def get_artist_ids_from_musicbrainz_googleSearch():
    # Connect to MongoDB
    client = pymongo.MongoClient()
    collection = client['musicbrainz']['spotify_googleSearch']
    # Get data
    cursor = collection.find({}, projection = {"_id": 0, "spotify_urls": 1})
    df = pd.DataFrame(cursor)
    # Remove empty record
    df = df.loc[df['spotify_urls'].map(bool)]
    # Explode lists
    df = df.explode(column='spotify_urls').reset_index(drop=True)
    # Parse spotify id
    df['artist_id'] = df['spotify_urls'].apply(parse_spotify_id)
    df = df[['artist_id']]
    # Remove duplicates
    df = df.drop_duplicates()
    return df

def get_artist_ids_from_grammy_googleSearch():
    # Connect to MongoDB
    client = pymongo.MongoClient()
    collection = client['grammyAwards']['artists_googleSearch']
    # Get data
    cursor = collection.find({}, projection = {"_id": 0, "links": 1})
    df = pd.DataFrame(cursor)
    # Remove empty record
    df = df.loc[df['links'].map(bool)]
    # Extract spotify urls
    spotify_urls = [i['Spotify'] for i in df['links'] if 'Spotify' in i]
    df = pd.DataFrame(spotify_urls, columns=['spotify_url'])
    # Parse spotify id
    df['artist_id'] = df['spotify_url'].apply(parse_spotify_id)
    df = df[['artist_id']]
    # Remove duplicates
    df = df.drop_duplicates()
    return df

def get_artist_ids_from_related_artist_spotifyAbout():
    # Connect to MongoDB
    client = pymongo.MongoClient()
    collection = client['grammyAwards']['spotify_about']
    # Get data
    cursor = collection.find({}, projection = {"_id": 0, "about": 1})
    df = pd.DataFrame(cursor)
    # Get urls
    df = df['about'].apply(lambda i: i['hrefs']).explode().reset_index(drop=True).dropna()
    urls = list(map(lambda i: i['href'], df))
    # Extract artist urls
    urls = [url for url in urls if 'open.spotify.com/artist' in url]
    # Extract artist ids
    ids = list(map(parse_spotify_id, urls))
    df = pd.DataFrame(ids, columns=['artist_id'])
    return df

def get_artist_ids_from_musixmatch():
    # Connect to MongoDB
    client = pymongo.MongoClient()
    collection = client['musixmatch']['cleaned_data']
    # Get data
    cursor = collection.find({}, projection = {"_id": 0, "spotifyId": 1})
    df = pd.DataFrame(cursor)
    # Get spotify track ids
    track_ids = [i for i in df['spotifyId'] if i]
    # Connect to destination collection
    collection = client['spotify']['artist_id']
    # Load Spotify credentials
    load_dotenv()
    # Get artist ids from track ids
    def batch(iterable, n=1):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]
    for _iter, chunk in tqdm(enumerate(batch(track_ids, 50))):
        artist_ids = []
        if _iter % 5 == 0:
            # Sign in
            spotify = sp.Spotify(
                auth_manager=credentials(
                    client_id=os.environ.get('_id'), 
                    client_secret=os.environ.get('_secret')
                    )
                )
        tracks = spotify.tracks(chunk)
        artists_in_tracks = [i['artists'] for i in tracks['tracks'] if i]
        for artists_in_track in artists_in_tracks:
            for artist in artists_in_track:
                artist_ids.append(artist['id'])
        # Remove duplicates
        artist_ids = list(set(artist_ids))
        # Insert data
        df = pd.DataFrame(artist_ids, columns=['artist_id'])
        document = df.to_dict('records')
        collection.insert_many(document)
        # Slow down the requesting speed to avoid banning
        time.sleep(random.randint(0, 3))
    return None

def insert_dataframe_to_mongo(df, db_name, collection_name):
    # Connect to MongoDB
    client = pymongo.MongoClient()
    collection = client[db_name][collection_name]
    # Insert data
    document = df.to_dict('records')
    collection.insert_many(document)
    return None

def remove_duplicates(by, db_name, collection_name):
    # Connect to MongoDB
    client = pymongo.MongoClient()
    collection = client[db_name][collection_name]
    
    # Get data
    cursor = collection.find({}, projection = {"_id": 1, by: 1})
    df = pd.DataFrame(cursor)
    
    # Find duplicates
    dup = df[by].duplicated()
    if sum(dup):
        dup_df = df[dup]
        to_remove_ids = dup_df['_id'].reset_index(drop=True)
        
        # Remove data from collection
        for _id in tqdm(to_remove_ids):
            query = {"_id": _id}
            delete = collection.delete_one(query)
    return None

def main():
    # # From Musicbrainz
    print("Accumulating IDs from Musicbrainz")
    artist_ids_from_musicbrainz = get_artist_ids_from_musicbrainz()
    insert_dataframe_to_mongo(df=artist_ids_from_musicbrainz, db_name='spotify', collection_name='artist_id')
    del artist_ids_from_musicbrainz
    
    # # From MusicbrainzGoogleSearch
    print("Accumulating IDs from MusicbrainzGoogleSearch")
    artist_ids_from_musicbrainz_googleSearch = get_artist_ids_from_musicbrainz_googleSearch()
    insert_dataframe_to_mongo(df=artist_ids_from_musicbrainz_googleSearch, db_name='spotify', collection_name='artist_id')
    del artist_ids_from_musicbrainz_googleSearch

    # # From GrammyGoogleSearch
    print("Accumulating IDs from GrammyGoogleSearch")
    artist_ids_from_grammy_googleSearch = get_artist_ids_from_grammy_googleSearch()
    insert_dataframe_to_mongo(df=artist_ids_from_grammy_googleSearch, db_name='spotify', collection_name='artist_id')
    del artist_ids_from_grammy_googleSearch

    # # From related artists in SpotifyAbout
    print("Accumulating IDs from SpotifyAbout")
    artist_ids_from_related_artist_spotifyAbout = get_artist_ids_from_related_artist_spotifyAbout()
    insert_dataframe_to_mongo(df=artist_ids_from_related_artist_spotifyAbout, db_name='spotify', collection_name='artist_id')
    del artist_ids_from_related_artist_spotifyAbout

    # From Musixmatch
    print("Accumulating IDs from Musixmatch")
    get_artist_ids_from_musixmatch()

    # Remove duplicate artist ids
    print("Start removing duplicate artist_id")
    remove_duplicates(by='artist_id', db_name='spotify', collection_name='artist_id')
    
if __name__ == "__main__":
    main()
