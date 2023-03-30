# CHANGE TO SELENIUM APPROACH

import scrapy
from imdb_professional.items import ImdbProfessionalItem
from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time
import re
import datetime

# Parameter preparation
# -- URLs
cast_ids = list()
urls = list()

# -- XPath
cast_name_xpath = '//h1/span/text()'
main_xpath = '//div[@class="sc-4390696d-3 dVbZNr"][1]//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-between ipc-metadata-list--base"]//li[@data-testid]'
movie_id_xpath = './/a[@class="ipc-metadata-list-summary-item__t"]'
movie_name_xpath = './/a[@class="ipc-metadata-list-summary-item__t"]'
movie_year_xpath = './/div[@class="ipc-metadata-list-summary-item__cc"]'
roles_xpath = './/div[@class="ipc-metadata-list-summary-item__tc"]/ul[1]/li//label'

class ImdbRoleSpider(scrapy.Spider):
    name = 'imdb_role'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/name/nm1500155']

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("start-maximized")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(1)
        see_all_button = self.driver.find_element(by=By.XPATH, value='//button[@data-testid="nm-flmg-paginated-all-actor"]')
        self.driver.execute_script("arguments[0].click();", see_all_button)
        time.sleep(3)

        # List of items
        main = driver.find_elements(by=By.XPATH, value=main_xpath)
        
        for i in main:
            # Create loader
            l = ItemLoader(item=ImdbProfessionalItem(), selector=i)
            
            # Key
            l.add_value('cast_id', re.search(r"\/(nm.+)\/", response.url).group(1))
            # l.add_xpath('cast_name', cast_name_xpath)
            l.add_value('movie_id', i.find_element(by=By.XPATH, value=movie_id_xpath).get_attribute('href'))
            l.add_value('movie_name', i.find_element(by=By.XPATH, value=movie_name_xpath).text)
            l.add_value('movie_year', i.find_element(by=By.XPATH, value=movie_year_xpath).text)
            l.add_value('roles', [elem.text for elem in i.find_elements(by=By.XPATH, value=roles_xpath)])

            # housekeeping fields
            l.add_value('url', response.url)
            l.add_value('spider', self.name)
            l.add_value('date', datetime.datetime.now().strftime('%d/%m/%Y'))
            
            yield l.load_item()
        self.driver.close()






from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

url = 'https://www.imdb.com/name/nm1500155'
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(url)

see_all_button = driver.find_element(by=By.XPATH, value='//button[@data-testid="nm-flmg-paginated-all-actor"]')
driver.execute_script("arguments[0].click();", see_all_button)