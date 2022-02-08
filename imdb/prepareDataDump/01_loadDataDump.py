# !/usr/bin/env python3
# encoding utf-8

"""
Download data from IMDB data dump: https://datasets.imdbws.com/
"""

import os
import re

def get_parent_dir_path():
    # get the parent directory name
    parent_dir = 'imdb'
    current_path = os.getcwd()
    # pattern: path end with 'imdb'
    pattern = f'.*{parent_dir}$'
    # get back by one level until arriving at the parent directory
    while not re.match(pattern=pattern, string=current_path):
        current_path = os.path.dirname(current_path)
    parent_dir_path = current_path
    return parent_dir_path

def setup_url():
    # get and store dumps   
    
    # params
    tables = [
        'name.basics',
        'title.akas',
        'title.basics',
        'title.crew',
        'title.episode',
        'title.principals',
        'title.ratings'
        ]
    
    xt = '.tsv.gz'
    
    base_url = 'https://datasets.imdbws.com/'
    
    target_urls = [base_url + table + xt for table in tables]
    return target_urls

def setup_destination(parent_dir_path):
    # destination folder
    folder = 'data'
    subfolder = 'imdb_dump'
    destination = os.path.join(parent_dir_path, folder, subfolder)    
    os.makedirs(destination, exist_ok=True)
    os.chdir(destination)
    return None

def download_and_extract(target_urls):
    # download item to destination folder
    for url in target_urls:
        # download
        d_cmd = ' '.join(['wget', url])
        os.system(d_cmd)
    
    # extract all .gz files
    e_cmd = ' '.join(['gunzip', '-f', '*.gz'])
    os.system(e_cmd)  
    return None

def main():
    # get parent directory path
    parent_dir_path = get_parent_dir_path()
    # setup target urls
    target_urls = setup_url()
    # setup destination path
    setup_destination(parent_dir_path)
    # download and extract files
    download_and_extract(target_urls)
    
if __name__ == '__main__':
    main()