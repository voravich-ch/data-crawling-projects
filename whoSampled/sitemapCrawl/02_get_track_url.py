# The ScraperAPI cannot bypass the bot detection at this stage (Download files).
# Hence, the approach is to use Zyte proxy.
# -- Note: After contacting ScraperAPI, the proxy could now bypass the bot detection.

import os
import re
import glob
import gzip
import shutil
import requests
import pymongo
import pandas as pd
from tqdm import tqdm

def get_parent_dir_path():
    # Get the project directory name
    parent_dir = 'whoSampled'
    current_path = os.getcwd()
    # Pattern: path end with 'whoSampled'
    pattern = f'.*{parent_dir}$'
    # Get back by one level until arriving at the parent directory
    while not re.match(pattern=pattern, string=current_path):
        current_path = os.path.dirname(current_path)
    parent_dir_path = current_path
    return parent_dir_path

def set_destination_path(parent_dir_path):
    # Destination folder
    folder = 'data'
    subfolder = 'sitemap'
    subfolder2 = 'track_url'
    destination = os.path.join(parent_dir_path, folder, subfolder, subfolder2)
    os.makedirs(destination, exist_ok=True)
    return destination

def get_track_url():
    client = pymongo.MongoClient()
    db = client['whoSampled']
    collection = db['sitemapURL']
    track_urls = [i['url'] for i in collection.find({}, projection = {"_id": 0, "url": 1}) if 'tracks' in i['url']]
    return track_urls

def download_files(track_urls, destination):
    # Set up Zyte
    proxy_host = 'proxy.zyte.com'
    proxy_port = '8011'
    proxy_auth = f'{API_KEY}:'
    proxies = {
        'https': 'http://{}@{}:{}/'.format(proxy_auth, proxy_host, proxy_port),
        'http': 'http://{}@{}:{}/'.format(proxy_auth, proxy_host, proxy_port)
        }
    
    # Download files
    for url in tqdm(track_urls):
        f_name = url.split('/')[-1]
        f_path = os.path.join(destination, f_name)
        response = requests.get(
            url,
            proxies=proxies,
            verify='zyte-smartproxy-ca.crt'
        )
        with open(f_path, 'wb') as f:
            f.write(response.content)

def extract_files(directory):
    # Extract .gz files
    f_paths = glob.glob(os.path.join(directory, '*.gz'))
    for f in f_paths:
        f_name = f.rsplit('.', 1)[0]
        with gzip.open(f, 'rb') as f_in, open(f_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(f)

def insert_to_mongo(directory):
    client = pymongo.MongoClient()
    db = client['whoSampled']
    collection = db['trackURL']
    f_paths = glob.glob(os.path.join(directory, '*.xml'))
    for f in tqdm(f_paths):
        df = pd.read_xml(f)
        df = df.rename(columns={'loc': 'url'})
        documents = df.to_dict('records')
        collection.insert_many(documents)

def main():
    parent_dir_path = get_parent_dir_path()
    destination = set_destination_path(parent_dir_path)
    track_urls = get_track_url()
    download_files(track_urls, destination)
    extract_files(directory=destination)
    insert_to_mongo(directory=destination)

if __name__ == "__main__":
    main()