import os
import re
import numpy as np
import pandas as pd
import pymongo

def set_path():
    # get the project directory name
    parent_dir = 'whoSampled'
    current_path = os.getcwd()
    # pattern: path end with 'whoSampled'
    pattern = r'.*whoSampled$'
    # get back by one level until arriving at the parent directory
    while not re.match(pattern=pattern, string=current_path):
        current_path = os.path.dirname(current_path)
    parent_dir_path = current_path
    # data folder
    folder = 'data'
    data_folder = os.path.join(parent_dir_path, folder)
    # set as working directory
    os.chdir(data_folder)
    return None

def read_json_line(f_name):
    # Read json file
    df = pd.read_json(f_name, orient="records", lines=True)
    return df

def clean_first_step(first_step):
    # There are 42 uncleaned data points – can be cleaned with drop duplicates
    first_step = first_step.drop_duplicates(subset=['response_url'])
    first_step.reset_index(inplace=True, drop=True)
    for i in range(len(first_step)):
        if isinstance(first_step['samples'][i], dict):
            first_step['samples'][i] = [first_step['samples'][i]]
        if isinstance(first_step['sampled'][i], dict):
            first_step['sampled'][i] = [first_step['sampled'][i]]     
    return first_step

def clean_second_step(second_step):
    # Prepare response url
    pattern = r'(.+)sample.+'
    regex = re.compile(pattern)
    second_step['response_url'] = list(map(lambda i: regex.search(i).group(1), second_step['response_url']))
    # Subset only relevant columns
    relevant_col = ['samples', 'sampled', 'response_url']
    second_step = second_step[relevant_col]
    # Concatenate data – those with more than one pages since we did not do pagination during scraping to optimise speed
    second_step = second_step.groupby('response_url').agg('sum').reset_index()
    # Format empty value
    second_step = second_step.replace(0, None)
    return second_step

def merge_whoSampled_data(first_step, second_step):
    # Subset only relevant columns
    relevant_col = ['samples', 'sampled', 'response_url']
    df1 = first_step[relevant_col]
    df2 = second_step[relevant_col]
    # Merge data
    df1 = df1.set_index('response_url')
    df2 = df2.set_index('response_url')
    df1.update(df2)
    # Update the main dataframe
    first_step['samples'] = df1['samples'].values
    first_step['sampled'] = df1['sampled'].values
    # Replace NaN with None for consistency
    first_step = first_step.replace(np.nan, None)
    return first_step

def insert_to_mongo(df):
    client = pymongo.MongoClient()
    db = client['whoSampled']
    collection = db['whoSampled']
    collection.insert_many(df.to_dict('records'))

def main():
    # Path setup
    set_path()
    # Read data
    first_step = read_json_line(f_name="first-step-whoSampled.jl")
    second_step = read_json_line(f_name="second-step-whoSampled.jl")
    # Clean data
    first_step = clean_first_step(first_step)
    second_step = clean_second_step(second_step)
    # Merge data
    whoSampled = merge_whoSampled_data(first_step, second_step)
    # Insert data to Mongo
    insert_to_mongo(df=whoSampled)

if __name__ == '__main__':
    main()
