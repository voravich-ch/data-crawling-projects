import os
import re

def get_parent_dir_path():
    # get the parent directory name
    parent_dir = 'rottenTomatoes'
    current_path = os.getcwd()
    # pattern: path end with 'rottenTomatoes'
    pattern = f'.*{parent_dir}$'
    # get back by one level until arriving at the parent directory
    while not re.match(pattern=pattern, string=current_path):
        current_path = os.path.dirname(current_path)
    parent_dir_path = current_path
    return parent_dir_path