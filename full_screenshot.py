from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os.path
from datetime import datetime


from selenium.webdriver.chrome.options import Options

from urllib.parse import urlparse

# # Initialize the Selenium WebDriver
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver', chrome_options  = options)
driver = webdriver.Chrome(options=options)


def take_screenshot(url_name):
    current_time = datetime.now()
    start_time = time.time()
    url = f"http://{url_name}/"
    #name 
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    ss_name = domain_name.split(".")[0]
    path = f"ss_test/{ss_name}.png"
    if os.path.isfile(path):
        print("Screenshot of url already exist:", ss_name)
        return path
    else:
        try:
            driver.get(url)
            time.sleep(10)
            
            S = lambda X: driver.execute_script(f'return document.body.parentNode.scroll{X}')
            #(S('Width'), S('Height'))
            driver.set_window_size(1920, 1080)
            
            driver.find_element(By.TAG_NAME, 'body').screenshot(path)
            print("Successfully extracted the screenshot of url:", ss_name," start time:",current_time)
            end_time = time.time()
            return path
        except:
            driver.save_screenshot(path)
            print("Successfully extracted the screenshot of url:", ss_name," start time:",current_time)
            end_time = time.time()
            return path

# df = pd.read_excel("../MC_w_text.xlsx",sheet_name= "Sheet1")
df = pd.read_csv("Main_data1.csv")

df['image_path1'] = df['url'].apply(take_screenshot)
# df['image_path'] = df.apply(
#     lambda row: take_screenshot(row['url']) if "Message" in row['image_path'] else row['image_path'], axis=1
# )
df.to_csv("Main_data1.csv",index=False)

driver.quit()


