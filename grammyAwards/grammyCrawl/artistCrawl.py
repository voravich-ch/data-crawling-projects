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

class grammyCrawler:
    
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        if self.driver:
            print("Selenium Status: Started")
    
    def process_web(self, url):
        while True:
            try:
                self.driver.get(url)
                break
            except TimeoutException:
                self.driver.refresh()
                print('Web not responding, refresh the page.')
        xpath = '//div[starts-with(@class, "bg-faint-gray-background border-t")]'
        buttons = self.driver.find_elements(by=By.XPATH, value=xpath)
        for button in buttons:
            button.click()
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

def connect_to_db(db_name, collection_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    return collection

def insert_data_to_mongo(data, collection):
    collection.insert_one(data)
