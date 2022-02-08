#!usr/bin/env python3

import os
import json
import pymongo

def connect_to_city(db_name, collection_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    return collection

def load_and_insert_data(f_name, collection):
    with open(f_name) as f:
        _json = json.load(f)
    collection.insert_many(_json)
    return None

collection = connect_to_city(db_name='rateYourMusic', collection_name='threads20211216')
load_and_insert_data(f_name='output.json', collection=collection)