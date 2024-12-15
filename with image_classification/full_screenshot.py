from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os.path
from datetime import datetime

from selenium.webdriver.chrome.options import Options

from urllib.parse import urlparse

# # # Initialize the Selenium WebDriver
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')

# # driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver', chrome_options  = options)
# driver = webdriver.Chrome(options=options)


def take_screenshot(url_name):

# # Initialize the Selenium WebDriver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver', chrome_options  = options)
    driver = webdriver.Chrome(options=options)

    try:
        current_time = datetime.now()
        start_time = time.time()
        url = f"http://{url_name}/"

        #name 
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc
        ss_name = domain_name.split(".")[0]
        path = f"ss/{ss_name}.png"

        driver.get(url)
        S = lambda X: driver.execute_script(f'return document.body.parentNode.scroll{X}')
        driver.set_window_size(1920, 1080)
        
        driver.find_element(By.TAG_NAME, 'body').screenshot(path)
        print("Successfully extracted the screenshot of url:", ss_name," start time:",current_time)
        end_time = time.time()
        driver.save_screenshot(path)
        driver.quit()
        return path
    except Exception as e:
        print(f"Failed to extract screenshot for {url_name}")
        driver.quit()
        return None
# url = "canadapharmacymedonline.com"
# image_path = take_screenshot(url)
# print(image_path)



