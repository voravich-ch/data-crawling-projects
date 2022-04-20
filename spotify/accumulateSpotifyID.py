import os
import re
import numpy as np
import pandas as pd
import pymongo

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

def insert_dataframe_to_mongo(df, db_name, collection_name):
    # Connect to MongoDB
    client = pymongo.MongoClient()
    collection = client[db_name][collection_name]
    # Insert data
    document = df.to_dict('records')
    collection.insert_many(document)
    return None

def main():
    # From Musicbrainz
    artist_ids_from_musicbrainz = get_artist_ids_from_musicbrainz()
    insert_dataframe_to_mongo(df=artist_ids_from_musicbrainz, db_name='spotify', collection_name='artist_id')
    
    # From MusicbrainzGoogleSearch
    artist_ids_from_musicbrainz_googleSearch = get_artist_ids_from_musicbrainz_googleSearch()
    insert_dataframe_to_mongo(df=artist_ids_from_musicbrainz_googleSearch, db_name='spotify', collection_name='artist_id')
    
    # From GrammyGoogleSearch
    artist_ids_from_grammy_googleSearch = get_artist_ids_from_grammy_googleSearch()
    insert_dataframe_to_mongo(df=artist_ids_from_grammy_googleSearch, db_name='spotify', collection_name='artist_id')
    
if __name__ == "__main__":
    main()
