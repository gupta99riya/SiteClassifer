import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from multiprocessing.pool import ThreadPool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pandas as pd
import numpy as np

# Set up Selenium WebDriver options (headless)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


# Function to scrape images from a given URL
def scrape_images_from_url(url_name):
    driver = webdriver.Chrome(options=options)
    current_time = datetime.now()
    start_time = time.time()

    url = f"http://{url_name}/"
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    ss_name = domain_name.split(".")[0]
    folder_path = f"scrape_images/{ss_name}"
    
    driver.get(url)
    time.sleep(10)  # Allow time for the page to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if os.path.exists(folder_path):
        return [os.path.join(folder_path, i) for i in os.listdir(folder_path + "/")]
        
    os.makedirs(folder_path, exist_ok=True)
    images = soup.findAll('img')
    
    count = 0
    image_sizes = {}
    downloaded_images = []  # To keep track of the image paths
    
    for image in images:
        count += 1
        image_src = image.get("src")
        if not image_src:
            continue  # Skip if no src attribute

        # Construct the full image URL
        image_url = image_src if image_src.startswith("http") else urljoin(url, image_src)
        
        try:
            response = requests.get(image_url)
            image_name = os.path.basename(image_url).split(".")[0] + str(count) + ".jpg"
            
            # Clean up if the URL contains query parameters
            if "?" in image_name:
                image_name = image_name.split("?")[0]
            
            image_path = os.path.join(folder_path, image_name)
            
            # Save the image
            with open(image_path, 'wb') as file:
                file.write(response.content)
            
            image_sizes[image_path] = os.path.getsize(image_path)
            downloaded_images.append(image_path)  # Add the image path to the list
            print(f"Downloaded: {image_name}")
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {image_url}: {e}")

    # Keep only the top N largest images
    N = 5
    if len(image_sizes) > N:
        sorted_images = sorted(image_sizes.items(), key=lambda item: item[1], reverse=True)
        images_to_keep = set(image[0] for image in sorted_images[:N])
        
        for image_path in image_sizes.keys():
            if image_path not in images_to_keep:
                os.remove(image_path)
                downloaded_images.remove(image_path)  # Remove from list if deleted
                print(f"Removed: {image_path}")
    
    driver.quit()
    return downloaded_images  # Return the list of image paths


# Function to process rows where extracted_images is empty or NaN
def process_row(row):
#     if pd.isna(row['extracted_images']) or not row['extracted_images']:
    return scrape_images_from_url(row['url'])
#     return row['extracted_images']


# Load URLs from the DataFrame (assuming an Excel file)
df = pd.read_excel("result.xlsx")  # Assuming your DataFrame is loaded from an Excel file with a 'url' column

# Use ThreadPool for parallel processing only on rows where extracted_images is NaN or empty
with ThreadPool() as pool:
    df['extracted_images'] = pool.map(process_row, [row for _, row in df.iterrows()])

# Save the updated DataFrame to a new CSV file (optional)
df.to_csv("updated_urls_with_images.csv", index=False)
