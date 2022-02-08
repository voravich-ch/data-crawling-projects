# !/usr/bin/env python3
# encoding utf-8

"""
Sampling titles from data dump
"""

import os
import re
import numpy as np
import pandas as pd

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

def setup_target(parent_dir_path):
    folder = 'dataDirectory'
    subfolder1 = 'imdb'
    subfolder2 = 'imdb_dump'
    ak_file = 'title.akas.tsv'
    bs_file = 'title.basics.tsv'
    ak_path = os.path.join(parent_dir_path, folder, subfolder1, subfolder2, ak_file)
    bs_path = os.path.join(parent_dir_path, folder, subfolder1, subfolder2, bs_file)
    return ak_path, bs_path

def read_data(file_path):
    # read tab-separated values files
    df = pd.read_csv(file_path, delimiter='\t', na_values=r'\N')
    return df
    
def sampling_data(ak, bs):
    '''
    Sampling criteria:
    
    A - released in the US 
    B - movie
    C - categorised
    '''
    # condition A
    ak.loc[:, 'us'] = 0
    ak.loc[ak['region'] == 'US', 'us'] = 1
    ak = ak.loc[ak['us'] > 0]
    ak.rename(columns={'titleId': 'tconst'}, inplace=True)
    df = pd.merge(ak, bs, on='tconst', how='left')
    
    # condition B
    df = df.loc[df['titleType'] == 'movie']
    
    # condition C
    selector = [len(str(i).split(',')) > 0 for i in df['genres']]
    df = df.loc[selector]
    
    # remove duplicates
    df = df.drop_duplicates(subset=['tconst'])
    
    # reset index
    df = df.reset_index(drop=True)
    return df

def setup_destination(parent_dir_path):
    # destination folder
    folder = 'data'
    destination = os.path.join(parent_dir_path, folder)
    os.makedirs(destination, exist_ok=True)
    os.chdir(destination)
    return None

def write_json(df):
    # write sliced data
    out_file = 'sample.json'
    df.to_json(out_file, orient='records')
    return None

def main():
    # get parent directory path
    parent_dir_path = get_parent_dir_path()
    # set target paths
    ak_path, bs_path = setup_target(parent_dir_path)
    # read data
    ak = read_data(ak_path)
    bs = read_data(bs_path)
    # sample data
    df = sampling_data(ak, bs)
    # setup destination path
    setup_destination(parent_dir_path)
    # write data as json
    write_json(df)

if __name__ == '__main__':
    main()

