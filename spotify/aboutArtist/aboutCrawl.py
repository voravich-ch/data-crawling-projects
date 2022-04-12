from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import re
import datetime
import requests
import bs4
import time
import pymongo
import pandas as pd

class spotifyAboutCrawler:
    
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("start-maximized")
        self.chrome_options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)

    def start_session(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                                       options=self.chrome_options)
        self.driver.implicitly_wait(10)
        if self.driver:
            self.item_count = 0
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
        print(f"Item Scraped Count: {self.item_count}")

    def insert_data_to_mongo(self, data, db_name, collection_name):
        # Connect to MongoDB
        client = pymongo.MongoClient()
        collection = db[db_name][collection_name]
        # Insert data
        collection.insert_one(data)
        self.item_count += 1

    def write_data_to_local(self, data, f_name):
        if os.path.exists(f_name):
            # Remove the file if it was created before the crawler start time
            if datetime.datetime.fromtimestamp(os.path.getctime(f_name)) < self.start_time:
                os.remove(f_name)
        with open(f_name, 'a+') as f:
            f.write(json.dumps(data) + "\n")
            self.item_count += 1
            
    def process_web(self, url):
        self.driver.get(url)
        xpath = '//button[starts-with(@class, "uhDzVbFHy")]'
        button = self.driver.find_element(by=By.XPATH, value=xpath)
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(0.5)
    
    def get_name(self):
        xpath = '//h1'
        name = self.driver.find_element(by=By.XPATH, value=xpath)
        if name:
            return name.text.strip()
    
    def get_rank(self):
        xpath = '//div[@class="ndIZG_atdpv_tBZtqQhk"]//div[@class="tQp8UOu8jGduQXUTcv0c"]'
        rank = self.driver.find_element(by=By.XPATH, value=xpath)
        if rank:
            return rank.text.strip().replace('\n', ' ')
    
    def get_followers(self):
        xpath = '//div[text()="Followers"]/preceding-sibling::div'
        followers = self.driver.find_element(by=By.XPATH, value=xpath)
        if followers:
            return followers.text.strip()
    
    def get_monthly_listeners(self):
        xpath = '//div[text()="Monthly Listeners"]/preceding-sibling::div'
        monthly_listeners = self.driver.find_element(by=By.XPATH, value=xpath)
        if monthly_listeners:
            return monthly_listeners.text.strip()
    
    def get_monthly_listeners_by_country(self):
        xpath = '//div[@class="Q_OUHp7iDNLBcO2ZYI2x"]'
        elements = self.driver.find_elements(by=By.XPATH, value=xpath)
        monthly_listeners_by_country = []
        for element in elements:
            country_xpath = 'div[@class="Type__TypeElement-goli3j-0 fWIEhj"]'
            listeners_xpath = 'div[@class="Type__TypeElement-goli3j-0 ebHsEf"]'
            country = element.find_element(by=By.XPATH, value=country_xpath)
            listeners = element.find_element(by=By.XPATH, value=listeners_xpath)
            monthly_listeners_by_country.append({
                "country": country.text.strip(),
                "listeners": re.search(r"[\d,]+", listeners.text.strip()).group(0)
            })
        return monthly_listeners_by_country
    
    def get_about(self):
        text_xpath = '//div[@class="Type__TypeElement-goli3j-0 gAmaez CjnwbSTpODW56Gerg7X6"]//p'
        elements = self.driver.find_elements(by=By.XPATH, value=text_xpath)
        text = '\n'.join([element.text.strip() for element in elements])
        hrefs_xpath = '//div[@class="Type__TypeElement-goli3j-0 gAmaez CjnwbSTpODW56Gerg7X6"]//a'
        elements = self.driver.find_elements(by=By.XPATH, value=hrefs_xpath)
        hrefs = []
        for element in elements:
            hrefs.append({
                "text": element.text.strip(),
                "href": element.get_attribute('href')
            })
        about = {
            "text": text,
            "hrefs": hrefs
        }
        return about

def get_urls_from_grammy(db_name, collection_name):
    client = pymongo.MongoClient()
    collection = db[db_name][collection_name]
    cursor = collection.find({}, projection = {"_id": 0, "links": 1})
    df = pd.DataFrame(cursor)
    spotify_urls = list(filter(None, [links.get('Spotify') for links in df['links'] if links]))
    return spotify_urls