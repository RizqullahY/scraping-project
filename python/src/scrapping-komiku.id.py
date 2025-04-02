import os
import os
import time
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def download_image(img_url, img_path, retries=5):
    for attempt in range(retries):
        try:
            img_data = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).content
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {img_path}")
            return
        except RequestException as e:
            print(f"Failed to download {img_url}, retrying... ({attempt+1}/{retries})")
            time.sleep(5)
    print(f"Failed to download {img_url} after {retries} attempts.")

def scrape_images():
    url = 'https://komiku.id/the-s-class-hunter-doesnt-want-to-be-a-villainous-princess-chapter-26/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img', itemprop='image')
        
        image_urls = [img['src'] for img in images if 'src' in img.attrs]
        
        # Extract chapter number from URL
        chapter = url.strip('/').split('-')[-1]
        folder_name = f"temp/{chapter}"
        os.makedirs(folder_name, exist_ok=True)
        
        for i, img_url in enumerate(image_urls, start=1):
            img_path = os.path.join(folder_name, f"image_{i}.jpg")
            download_image(img_url, img_path)
    else:
        print(f"Failed to fetch page, status code: {response.status_code}")

if __name__ == '__main__':
    scrape_images()
