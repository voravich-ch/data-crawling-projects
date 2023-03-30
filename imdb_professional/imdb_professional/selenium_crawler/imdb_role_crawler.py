from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time
import re
import datetime

class ImdbRoleCrawler:

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("start-maximized")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0")
        self.mongo_uri = 'mongodb://127.0.0.1:27018'

    def start_session(self):    
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        if self.driver:
            self.driver.implicitly_wait(10)
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
        print(f"Item Scraped Count (MongoDB): {self.item_count_mongo}")
    
    def get_role_data(self, url, collection):
        # Prepare parameters
        cast_name_xpath = '//h1/span'
        main_xpath = '//div[@class="sc-4390696d-3 dVbZNr"][1]//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-between ipc-metadata-list--base"]//li[@data-testid]'
        movie_id_xpath = './/a[@class="ipc-metadata-list-summary-item__t"]'
        movie_name_xpath = './/a[@class="ipc-metadata-list-summary-item__t"]'
        movie_year_xpath = './/div[@class="ipc-metadata-list-summary-item__cc"]'
        roles_xpath = './/div[@class="ipc-metadata-list-summary-item__tc"]/ul[1]/li//span[@class="ipc-metadata-list-summary-item__li"]'

        # Request page
        self.driver.get(url)
        time.sleep(2)
        
        # Click see all button
        try:
            see_all_button = self.driver.find_element(by=By.XPATH, value='//button[contains(@data-testid, "nm-flmg-paginated-all")]')
            self.driver.execute_script("arguments[0].click();", see_all_button)
            time.sleep(2)
        except:
            pass # The number of roles is small and thus there is no "See all" button

        
        # Extract data
        main = self.driver.find_elements(by=By.XPATH, value=main_xpath)
        for row in main:
            cast_id = re.search(r"\/(nm.+)", url).group(1)
            try:
                cast_name = self.driver.find_element(by=By.XPATH, value=cast_name_xpath).text
            except:
                cast_name = ''
            try:
                movie_id = row.find_element(by=By.XPATH, value=movie_id_xpath).get_attribute('href')
                movie_id = re.search(r'tt\d+', movie_id).group(0)
            except:
                movie_id = ''
            try:
                movie_name = row.find_element(by=By.XPATH, value=movie_name_xpath).text
            except:
                movie_name = ''
            try:
                movie_year = row.find_element(by=By.XPATH, value=movie_year_xpath).text
            except:
                movie_year = ''
            try:
                roles = [elem.text for elem in row.find_elements(by=By.XPATH, value=roles_xpath)]
            except:
                roles = []
            scrape_date = datetime.datetime.now().strftime('%d/%m/%Y')
            scrape_url = url
            # Structure record
            record = {
                "cast_id": cast_id,
                "cast_name": cast_name,
                "movie_id": movie_id,
                "movie_name": movie_name,
                "movie_year": movie_year,
                "roles": roles,
                "scrape_date": scrape_date,
                "scrape_url": scrape_url
            }
            # Insert data to mongo
            collection.insert_one(record)
            self.item_count_mongo += 1
            print(f'Total item inserted to Mongo: {self.item_count_mongo}')