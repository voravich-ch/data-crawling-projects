#!usr/bin/env python3

import os
import re
import pymongo
import json
import pandas as pd
import requests
import bs4
import time
from tqdm import tqdm
import multiprocessing, functools

def connect_to_city(db_name, collection_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    return collection

def get_data(collection):
    cursor = collection.find({}, projection = {"_id": 0})
    df = pd.DataFrame(cursor)
    df.drop_duplicates(subset=['name'], inplace=True)
    names = df['name'].dropna()
    names = names.str.replace(' ', '+').reset_index(drop=True)
    return names

def construct_urls(names):
    base_url = 'https://www.google.com/search?q='
    urls = [f'{base_url}{name}+musician' for name in names]
    return urls

def request_data(i):
    response = requests.get(urls[i],
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
                            )
    print(f'Status Code: {response.status_code}')
    retry = 0
    while response.status_code == 503:
        response = requests.get(urls[i],
                                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
                            )
        retry = retry + 1
        if retry == int(max_retry):
            print(f'Max retry attempt reached for: {response.url}.')
            break
    if response.status_code == 200:
        print(response.url)
        html_page = bs4.BeautifulSoup(response.content, 'html.parser')
        # Collect sidebar
        name = html_page.select_one('div.SPZz6b h2').get_text(strip=True) if html_page.select_one('div.SPZz6b h2') else None
        role = html_page.select_one('div.wwUB2c span').get_text(strip=True) if html_page.select_one('div.wwUB2c span') else None
        website = html_page.select_one('span.ellip').get_text(strip=True) if html_page.select_one('span.ellip') else None
        description = html_page.select_one('div.kno-rdesc span').get_text(strip=True) if html_page.select_one('div.kno-rdesc span') else None
        born = html_page.find('a', text='Born').parent.find_next_sibling().get_text() if html_page.find('a', text='Born') else None
        died = html_page.find('a', text='Died').parent.find_next_sibling().get_text() if html_page.find('a', text='Died') else None
        links = html_page.select('table.RJuLSb tr')
        if links:
            output = {}
            for link in links:
                output[link.get_text(strip=True)] = link.select_one('a')['href']
            links = output.copy()
        # Search query
        query = re.search(r'q=(.+)+musician', urls[i]).group(1).replace('+', ' ').strip()
        # Get wiki url
        wiki = html_page.select_one('div.yuRUbf a[href^="https://en.wikipedia.org"]')
        if wiki:
            wiki_url = wiki['href']
            response = requests.get(wiki_url,
                                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
                            )
            wiki_html = str(bs4.BeautifulSoup(response.content, 'html.parser'))
        else:
            wiki_html = None
        # Construct a document
        document = {
            "name": name,
            "role": role,
            "website": website,
            "description": description,
            "born": born,
            "died": died,
            "links": links,
            "query": query,
            "wiki_html": wiki_html,
        }
        # Insert the document to MongoDB
        collection = connect_to_city(db_name='grammyAwards', collection_name='artists_googleSearch')
        collection.insert_one(document)
        time.sleep(5)

# Parameter preparation
collection = connect_to_city(db_name='grammyAwards', collection_name='artists')
names = get_data(collection)
urls = construct_urls(names)

# Multiprocesing
# Start crawling
max_retry = input('Enter max retry attempt: ')
assert int(max_retry) >= 0, 'Max retry should be an integer equal or greater than 0'
print('Start crawling...')
print(f'Total pages: {len(urls)}')
num_processors = 1
with multiprocessing.Pool(num_processors) as p:
    list(tqdm(p.imap(request_data, list(range(len(urls)))), total = len(urls)))
print('Finished!')
