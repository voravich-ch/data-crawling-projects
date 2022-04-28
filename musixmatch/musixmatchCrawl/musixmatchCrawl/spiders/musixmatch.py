#!usr/bin/env python3

import os
import re
import pymongo
import pandas as pd
from tqdm import tqdm

def connect_to_city(db_name, collection_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    return collection

def load_and_insert_data(f_name, collection):
    chunks = pd.read_json(f_name, orient='records', lines=True, chunksize=20000)
    for df in tqdm(chunks):
        # Remove duplicates (Obsolete track ids)
        # row_select = df.apply(lambda i: i['variables']['track']['id'] == int(re.search('\d+', i['request_url']).group(0)), axis=1)
        # -- vectorized approach above is efficient but not for this case because some records were not properly formatted
        for i in tqdm(range(len(df))):
            try:
                check = df.iloc[i]['variables']['track']['id'] == int(re.search('\d+', df.iloc[i]['request_url']).group(0))
                if check:
                    # Insert to Mongo
                    document = df.iloc[i].to_dict()
                    collection.insert_one(document)
            except:
                pass
    os.rename(f_name, f'up_{f_name}')

def main():
    collection = connect_to_city(db_name='musixmatch', collection_name='data')
    load_and_insert_data(f_name='555813_240000000.jl', collection=collection)
    
if __name__ == "__main__":
    main()
