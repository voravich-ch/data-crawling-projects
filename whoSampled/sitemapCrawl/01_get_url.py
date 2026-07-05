# Scrape urls from whoSampled sitemap
# To scrape data from whoSampled, a proxy is needed (Tor and Cloud VM do not work)
# Scraperapi provides free service for 5000 requests per month – 100k for $49; 1M for $149
# Sample request url: "http://api.scraperapi.com?api_key={your_api_key}&url=https://www.whosampled.com/Kanye-West/"

import os
import re
import requests
import bs4
import json
import pandas as pd
from itemadapter import ItemAdapter

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
    destination = os.path.join(parent_dir_path, folder, subfolder)
    os.makedirs(destination, exist_ok=True)
    return destination

def request_data():
    # Prepare url
    api_key = API_KEY
    url = 'https://www.whosampled.com/static/sitemaps/sitemap.xml'
    request_url =  f'http://api.scraperapi.com?api_key={api_key}&url={url}'
    # Request data
    response = requests.get(request_url)
    # Parse xml
    xml = bs4.BeautifulSoup(response.content, 'xml')
    # Get urls
    urls = xml.find_all('loc')
    urls = [url.get_text() for url in urls]
    df = pd.DataFrame(data=urls, columns=['url'])
    return df

def write_data(data, destination):
    f_name = 'sitemap_url.jl'
    f_path = os.path.join(destination, f_name)
    with open(f_path, 'a+') as f:
        for record in data.to_dict('records'):
            line = json.dumps(record) + "\n"
            f.write(line)

def main():
    parent_dir_path = get_parent_dir_path()
    destination = set_destination_path(parent_dir_path)
    df = request_data()
    write_data(data=df, destination=destination)
    print('Process completed.')

if __name__ == "__main__":
    main()
