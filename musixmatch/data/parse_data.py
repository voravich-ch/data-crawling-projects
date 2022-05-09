import pymongo
import numpy as np
import pandas as pd
from tqdm import tqdm

# Extract only relevant fields

# Connect to db
client = pymongo.MongoClient()
db = client['musixmatch']
collection = db['data']

# Get data
cursor = collection.find({})

# Connect to clean collection
collection = db['cleaned_data']

for record in tqdm(cursor):
    document = {
        "musixmatchId": record['variables']['track']['id'],
        "spotifyId": record['variables']['track']['spotifyId'],
        "soundcloudId": record['variables']['track']['soundcloudId'],
        "xboxmusicId": record['variables']['track']['xboxmusicId'],
        "rating": record['variables']['track']['rating'],
        "length": record['variables']['track']['length'],
        "numFavourite": record['variables']['track']['numFavourite'],
        "albumId": record['variables']['track']['albumId'],
        "albumName": record['variables']['track']['albumName'],
        "artistId": record['variables']['track']['artistId'],
        "artistName": record['variables']['track']['artistName'],
        "firstReleaseDate": record['variables']['track']['firstReleaseDate'],
        "primaryGenres": record['variables']['track']['primaryGenres'],
        "secondaryGenres": record['variables']['track']['secondaryGenres'],
        "lyrics": record['variables']['lyrics']['lyrics']['body'] if record['variables']['lyrics']['lyrics'] else None,
        "lyrics_language": record['variables']['lyrics']['lyrics']['language'] if record['variables']['lyrics']['lyrics'] else None,
        "request_url": record['request_url'],
        "response_url": record['response_url'],
        "spider": record['spider'],
        "crawl_date": record['crawl_date']
    }
    insert = collection.insert_one(document)

