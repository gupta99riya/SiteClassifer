from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import requests
import os 

# # Initialize the Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--disable-dev-shm-usage')

# driver = webdriver.Chrome(options=options)

error_strings=['Visit cloudflare.com for more information','Error code','Enable JavaScript and cookies to continue','Verifying you are human','Verify you are human','Sorry, you have been blocked']

def check_string_in_list(target_string, string_list = error_strings):
    # Convert target string to lowercase and check each substring in the list (also in lowercase)
    return bool(list(filter(lambda x: x.lower() in target_string.lower(), string_list)))

def scrapper(url,output_folder="scrape_files_final/"):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    domain = url.replace("https://","").replace("http://","").replace("www.","")
    main_url = f"http://{domain.strip()}"
    try:
        response = requests.get(main_url)
        # response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        stripped_text = '\n'.join(soup.stripped_strings)
        if check_string_in_list(stripped_text):
            return f"Error in scrapping for {url}"
        filename = domain.replace(".","_").replace("/","__")+'.txt'
        with open(output_folder+filename, 'w', encoding='utf-8') as f:
            f.write(stripped_text)
        print(f"Successfully saved url {url} scrapped text {output_folder}{filename}")
    except Exception as e:
        print("Error2 in scrapping for ",url,f": {e}")
        driver = webdriver.Chrome(options  = chrome_options)
        try:
            driver.get(main_url)
            time.sleep(5)
            # Parse the webpage content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            stripped_text = '\n'.join(soup.stripped_strings)
            if check_string_in_list(stripped_text):
                return f"Error in scrapping for {url}"
            
            filename = domain.replace(".","_").replace("/","__")+'.txt'
            with open(output_folder+filename, 'w', encoding='utf-8') as f:
                f.write(stripped_text)
            print(f"Successfully saved url {url} scrapped text {output_folder}{filename}")
            driver.quit()
        except Exception as e:
            print("Error in scrapping for ",url,f": {e}")
    return stripped_text
