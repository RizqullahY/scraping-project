import os
import sys
import time
import requests
import shutil
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def download_image(img_url, img_path, retries=5):
    for attempt in range(retries):
        try:
            img_data = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).content
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {img_path}")
            return
        except RequestException:
            print(f"Failed to download {img_url}, retrying... ({attempt+1}/{retries})")
            time.sleep(5)
    print(f"Failed to download {img_url} after {retries} attempts.")

def scrape_images_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img', itemprop='image')
        
        image_urls = [img['src'] for img in images if 'src' in img.attrs]

        # Ambil judul halaman
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text.strip()
            valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            folder_name = ''.join(c for c in title if c in valid_chars)
        else:
            folder_name = url.strip('/').split('/')[-1]

        folder_path = os.path.join(SCRIPT_DIR, "temp", folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Menyalin index.html
        index_source = os.path.join(SCRIPT_DIR, 'index.html')
        index_dest = os.path.join(folder_path, 'index.html')
        try:
            shutil.copy(index_source, index_dest)
            print(f"Copied index.html to {folder_path}")
        except FileNotFoundError:
            print("index.html tidak ditemukan!")

        for i, img_url in enumerate(image_urls, start=1):
            img_path = os.path.join(folder_path, f"image_{i}.jpg")
            download_image(img_url, img_path)
    else:
        print(f"Failed to fetch page {url}, status code: {response.status_code}")

if __name__ == '__main__':
    txt_path = os.path.join(SCRIPT_DIR, "all-chapter.txt")

    START_LINE = 1
    END_LINE = 5

    if os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
            urls_reversed = urls[::-1] 
            selected_urls = urls_reversed[1:END_LINE - START_LINE]
            selected_urls = selected_urls[::-1] 
            for chapter_url in selected_urls:
                scrape_images_from_url(chapter_url)

    else:
        print(f"Tidak ditemukan file: {txt_path}")

