#!usr/bin/env python3

import os
import re
import pymongo
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import multiprocessing, functools
from dotenv import load_dotenv

def connect_to_city(db_name, collection_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    return collection

def get_data(collection):
    cursor = collection.find({}, projection = {"_id": 0})
    df = pd.DataFrame(cursor)
    df.drop_duplicates(subset=['artist_id'], inplace=True)
    df = df[df['name'] != 'Deleted Artist']
    names = df['name'].dropna()
    names = names.str.replace(' ', '+').reset_index(drop=True)
    return names

def construct_urls(names):
    base_url = 'https://www.google.com/search?q='
    urls = [f'{base_url}{name}+site%3Aopen.spotify.com%2Fartist' for name in names]
    return urls

def get_parent_dir_path():
    # get the project directory name
    parent_dir = 'googleSearch'
    current_path = os.getcwd()
    # pattern: path end with 'googleSearch'
    pattern = r'.*googleSearch$'
    # get back by one level until arriving at the parent directory
    while not re.match(pattern=pattern, string=current_path):
        current_path = os.path.dirname(current_path)
    parent_dir_path = current_path
    return parent_dir_path

def setup_destination(parent_dir_path, f_name):
    # destination folder
    folder = 'dataCollection'
    subfolder = 'data'
    destination = os.path.join(parent_dir_path, folder, subfolder)
    os.makedirs(destination, exist_ok=True)
    out_file = os.path.join(destination, f_name)
    return out_file

def request_data(i):
    response = requests.get(
        urls[i],
        proxies=proxies,
        verify='zyte-smartproxy-ca.crt',
        headers={'X-Crawlera-Debug-UA': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533+ (KHTML, like Gecko)',
                 'X-Crawlera-Region': 'CA'}
    )
    print(f'Status Code: {response.status_code}')
    retry = 0
    while response.status_code == 503:
        response = requests.get(
        urls[i],
        proxies=proxies,
        verify='zyte-smartproxy-ca.crt',
        headers={'X-Crawlera-Debug-UA': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533+ (KHTML, like Gecko)',
                 'X-Crawlera-Region': 'CA'})
        retry = retry + 1
        if retry == int(max_retry):
            print(f'Max retry attempt reached for: {response.url}.')
            break
    if response.status_code == 200:
        print(response.url)
        if re.search(r'q=(.+\+)site', response.url): # Sometimes the request was redirected to another url
            html_page = BeautifulSoup(response.content, 'html.parser')
            a_tags = html_page.select('div.yuRUbf a[href^="https://open.spotify.com/artist/"]')
            spotify_urls = [a.get('href') for a in a_tags]
            query = re.search(r'q=(.+\+)site', response.url).group(1).replace('+', ' ').strip()
            document = {
                "spotify_urls": spotify_urls,
                "query": query
            }
            with open(out_file, 'a+') as f:
                f.write(json.dumps(document) + "\n")

def main():
    # Parameter preparation
    collection = connect_to_city(db_name='musicbrainz', collection_name='artists_to_search')
    names = get_data(collection)
    urls = construct_urls(names)
    out_file = setup_destination(get_parent_dir_path(), f_name='searchArtist_parallel.jl')
    
    # Zyte
    proxy_host = os.environ.get('PROXY_HOST')
    proxy_port = os.environ.get('PROXY_PORT')
    proxy_auth = os.environ.get('ZYTE_SMARTPROXY_APIKEY')
    proxies = {"https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
               "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}
    
    # Multiprocesing
    # Start crawling
    max_retry = input('Enter max retry attempt: ')
    assert int(max_retry) >= 0, 'Max retry should be an integer equal or greater than 0'
    print('Start crawling...')
    print(f'Total pages: {len(urls)}')
    num_processors = 10
    with multiprocessing.Pool(num_processors) as p:
        list(tqdm(p.imap(request_data, list(range(len(urls)))), total = len(urls)))
    print('Finished!')

if __name__ == "__main__":
    main()