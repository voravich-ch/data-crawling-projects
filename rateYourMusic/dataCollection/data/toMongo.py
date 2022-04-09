#!usr/bin/env python3

import os
import re
import pymongo
import pandas as pd

def connect_to_city(db_name, collection_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    return collection

def load_and_insert_data(f_name, collection):
    df = pd.read_json(f_name, orient='records', lines=True)
    documents = df.to_dict('records')
    collection.insert_many(documents)
    
def main():
    collection = connect_to_city(db_name='rateYourMusic', collection_name='genre_level')
    load_and_insert_data(f_name='00_genre-level.jl', collection=collection)
    
if __name__ == "__main__":
    main()