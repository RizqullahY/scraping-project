import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

current_dir = os.path.dirname(os.path.abspath(__file__))

def scrape_judulseries(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ambil judul halaman dan bersihkan untuk nama file
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text.strip()
            valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            safe_title = ''.join(c for c in title if c in valid_chars).replace(' ', '_')
        else:
            safe_title = "output"

        output_file = os.path.join(current_dir, f"{safe_title}.txt")

        # Ambil semua elemen chapter
        judulseries_elements = soup.find_all('td', class_='judulseries')

        urls = []
        for elem in judulseries_elements:
            link_tag = elem.find('a')
            if link_tag and 'href' in link_tag.attrs:
                relative_href = link_tag['href']
                full_url = urljoin(url, relative_href)
                urls.append(full_url)

        urls.reverse()  # Biar chapter terbaru ada di paling atas

        with open(output_file, 'w', encoding='utf-8') as f:
            for i, link in enumerate(urls, start=1):
                f.write(f"{link}\n")

        print(f"Hasil disimpan ke '{output_file}'")
    else:
        print(f"Failed to fetch page {url}, status code: {response.status_code}")

if __name__ == '__main__':
    url = "https://komiku.id/manga/omniscient-readers-viewpoint/" 
    scrape_judulseries(url)
