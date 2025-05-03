import os
import time
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def save_container_html(h1_title, content_html, folder_path, filename='index.html'):
    full_html = f"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{h1_title}</title>
        <link rel="stylesheet" href="../../style.css">
        <script src="../../../lib/jquery.js"></script>
    </head>
    <body>
        <div class="scroll-controls-container">
            <div class="scroll-controls">
                <label for="scroll-speed" class="scroll-label">Scroll:</label>
                <select id="scroll-speed" class="scroll-select">
                <option value="1">1</option>
                <option value="2" selected>2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                </select>

                <button id="start-scroll" class="scroll-button start">Mulai</button>
                <button id="stop-scroll" class="scroll-button stop" disabled>
                Henti
                </button>
                <button id="fullscreen-button" class="scroll-button fullscreen">
                Fullscreen
                </button>
                <form action="../../temp/" target="_blank" style="display: inline;">
                    <button type="submit" class="scroll-button temp-button">T</button>
                </form>        
            </div>
            </div>
        <h1>{h1_title}</h1>
        {content_html}
        <script src="../../../js/autoscroll.js"></script>
        <script src="../../../js/fullscreen.js"></script>
    </body>
</html>
"""
    
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Saved HTML content to: {file_path}")

def scrape_container(chapter):
    url = f'https://bacalightnovel.co/the-villain-wants-to-live-chapter-{chapter}/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        print(f"Failed to fetch page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Ambil judul dari <div class="epheader"> > <h1>
    h1_title = "Chapter"
    epheader_div = soup.find('div', class_='epheader')
    if epheader_div:
        h1_tag = epheader_div.find('h1')
        if h1_tag:
            h1_title = h1_tag.get_text(strip=True)

    # Ambil isi dari <div class="epcontent">
    container_div = soup.find('div', class_='text-left')
    if not container_div:
        print("div.epcontent not found on the page.")
        return

    # Ambil judul halaman untuk nama folder
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.strip()
        valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        folder_name = ''.join(c for c in title if c in valid_chars)
    else:
        folder_name = url.strip('/').split('/')[-1]

    folder_path = os.path.join(SCRIPT_DIR, "temp", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Simpan gabungan judul dan konten
    save_container_html(h1_title, str(container_div), folder_path)

if __name__ == '__main__':
    first_chapter = 30
    until_chapter = 50
    for chapter in range(first_chapter, until_chapter + 1 ):
        scrape_container(chapter)
