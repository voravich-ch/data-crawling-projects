#!usr/bin/env python3

import os
import json
import pymongo
import pandas as pd

def connect_to_city(db_name, collection_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    return collection

def load_and_insert_data(f_name, collection):
    df = pd.read_json(f_name, lines=True)
    document = df.to_dict('records')
    collection.insert_many(document)
    return None

def main():
    collection = connect_to_city(db_name='musixmatch', collection_name='test')
    load_and_insert_data(f_name='musixmatch.jl', collection=collection)
    
if __name__ == "__main__":
    main()