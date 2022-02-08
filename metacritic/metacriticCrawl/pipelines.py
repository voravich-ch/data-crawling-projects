# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting


# useful for handling different item types with a single interface
import os
import re
import json
from datetime import datetime
from itemadapter import ItemAdapter

class JsonWriterPipeline:

    def open_spider(self, spider):
        
        def get_parent_dir_path():
            # get the parent directory name
            parent_dir = 'metacritic'
            current_path = os.getcwd()
            # pattern: path end with 'metacritic'
            pattern = f'.*{parent_dir}$'
            # get back by one level until arriving at the parent directory
            while not re.match(pattern=pattern, string=current_path):
                current_path = os.path.dirname(current_path)
            parent_dir_path = current_path
            return parent_dir_path
        
        def setup_destination(parent_dir_path):
            # destination folder
            folder = 'data'
            destination = os.path.join(parent_dir_path, folder)
            return destination
        
        parent_dir_path = get_parent_dir_path()
        destination = setup_destination(parent_dir_path)
        os.makedirs(destination, exist_ok=True)
        file_name = f'{spider.name}.jl'
        out_file = os.path.join(destination, file_name)
        
        self.file = open(out_file, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
