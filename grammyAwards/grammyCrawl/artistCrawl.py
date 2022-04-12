from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import os
import re
import datetime
import json
import requests
import bs4
import time
import pymongo

class grammyCrawler:
    
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("start-maximized")
        self.chrome_options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)

    def start_session(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                                       options=self.chrome_options)
        if self.driver:
            self.item_count_local = 0
            self.item_count_mongo = 0
            self.start_time = datetime.datetime.now()
            print("Selenium Status: Started")
            print(f"Start Time: {self.start_time.strftime('%m/%d/%Y, %H:%M:%S')}")

    def end_session(self):
        self.driver.quit()
        print("Selenium Status: Finished")
        self.finish_time = datetime.datetime.now()
        print(f"Start Time: {self.start_time.strftime('%m/%d/%Y, %H:%M:%S')}")
        print(f"Finish Time: {self.finish_time.strftime('%m/%d/%Y, %H:%M:%S')}")
        print(f"Total Execution Time: {str(self.finish_time - self.start_time).split('.')[0]}")
        print(f"Item Scraped Count (Local): {self.item_count_local}")
        print(f"Item Scraped Count (MongoDB): {self.item_count_mongo}")

    def insert_data_to_mongo(self, data, db_name, collection_name):
        # Connect to MongoDB
        client = pymongo.MongoClient()
        collection = db[db_name][collection_name]
        # Insert data
        collection.insert_one(data)
        self.item_count_mongo += 1

    def write_data_to_local(self, data, f_name):
        if os.path.exists(f_name):
            # Remove the file if it was created before the crawler start time
            if datetime.datetime.fromtimestamp(os.path.getctime(f_name)) < self.start_time:
                os.remove(f_name)
        with open(f_name, 'a+') as f:
            f.write(json.dumps(data) + "\n")
            self.item_count_local += 1

    def process_web(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        xpath = '//div[starts-with(@class, "bg-faint-gray-background border-t")]'
        buttons = self.driver.find_elements(by=By.XPATH, value=xpath)
        for button in buttons:
            self.driver.execute_script("arguments[0].click();", button)
            time.sleep(0.5)
    
    def get_name(self):
        xpath = '//h1'
        name = self.driver.find_element(by=By.XPATH, value=xpath)
        return name.text.strip()
    
    def get_wins(self):
        xpath = '//h4[text()="WINS*"]/following::h1'
        wins = self.driver.find_element(by=By.XPATH, value=xpath)
        return wins.text.strip()
    
    def get_nominations(self):
        xpath = '//h4[text()="NOMINATIONS*"]/following::h1'
        nominations = self.driver.find_element(by=By.XPATH, value=xpath)
        return nominations.text.strip()
    
    def get_awards_and_nominations(self):
        xpath = '//div[starts-with(@class, "bg-white border-t")]'
        elements = self.driver.find_elements(by=By.XPATH, value=xpath)
        awards_and_nominations = {}
        for element in elements:
            year, wins, nominations = self.parse_awards_and_nominations(element)
            awards_and_nominations[year] = {
                'wins': wins,
                'nominations': nominations
            }
        return awards_and_nominations
    
    def parse_awards_and_nominations(self, element):
        html = bs4.BeautifulSoup(element.get_attribute('innerHTML'), 'html.parser')
        year = html.find('h2').get_text()
        
        if html.find(text='Wins'):
            awards = html.find(text="Wins").findNext('div')
            wins = []
            for award in list(awards):
                try:
                    record = {
                        "award": award.find('h2').get_text().strip(),
                        "release": award.find('h3').get_text().strip()
                    }
                    wins.append(record)
                except:
                    pass
        else:
            wins = None
        
        if html.find(text='Nominations'):
            awards = html.find(text="Nominations").findNext('div')
            nominations = []
            for award in list(awards):
                try:
                    record = {
                        "award": award.find_all('h4')[0].get_text().strip(),
                        "release": award.find_all('h4')[1].get_text().strip()
                    }
                    nominations.append(record)
                except:
                    pass
        else:
            nominations = None
        return year, wins, nominations

def parse_start_urls():
    sitemap_url = 'https://www.grammy.com/sitemap.xml'
    response = requests.get(sitemap_url)
    html = bs4.BeautifulSoup(response.text, 'html.parser')
    find_artist = re.compile(r'https://www.grammy.com/artists/.+/\d+')
    artist_urls = [url.get_text() for url in html.find_all('loc') if find_artist.match(url.get_text())]
    return artist_urls
