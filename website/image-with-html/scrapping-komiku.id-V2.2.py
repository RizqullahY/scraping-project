import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../module")))
import time
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import shutil 
from title import get_url_by_number  

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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

def scrape_images(url_number , chapter):
    url = get_url_by_number(url_number, chapter)
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
            # Bersihkan judul dari karakter yang tidak valid untuk nama folder
            valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            folder_name = ''.join(c for c in title if c in valid_chars)
        else:
            # Jika judul tidak ditemukan, gunakan bagian akhir URL
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
            print("index.html tidak ditemukan di direktori utama!")
        
        for i, img_url in enumerate(image_urls, start=1):
            img_path = os.path.join(folder_path, f"image_{i}.jpg")
            download_image(img_url, img_path)
    else:
        print(f"Failed to fetch page, status code: {response.status_code}")

if __name__ == '__main__':
    first_chapter = 1
    until_chapter = 3
    for chapter in range(first_chapter, until_chapter + 1):
        scrape_images(url_number = 2, chapter = chapter)
        # URL NUMBER BISA DILIHAT DI title.py