import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def scrape(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text.strip()
            valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            safe_title = ''.join(c for c in title if c in valid_chars).replace(' ', '_')
        else:
            safe_title = "output"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(current_dir, f"{safe_title}.txt")

        judulseries_elements = soup.find_all('td', class_='judulseries')

        urls = []
        for elem in judulseries_elements:
            link_tag = elem.find('a')
            if link_tag and 'href' in link_tag.attrs:
                relative_href = link_tag['href']
                full_url = urljoin(url, relative_href)
                urls.append(full_url)

        urls.reverse()

        with open(output_file, 'w', encoding='utf-8') as f:
            for link in urls:
                f.write(f"{link}\n")

        messagebox.showinfo("Berhasil", f"Hasil disimpan ke:\n{output_file}")
    else:
        messagebox.showerror("Gagal", f"Status code: {response.status_code}")

# GUI hanya untuk testing / standalone run
def run_gui():
    def start_scraping():
        url = url_entry.get().strip()
        if not url:
            messagebox.showwarning("Peringatan", "URL tidak boleh kosong!")
            return
        scrape(url)

    root = tk.Tk()
    root.title("Komiku Scraper")

    tk.Label(root, text="Masukkan URL Manga (komiku.id):").pack(padx=10, pady=(10, 2))

    url_entry = tk.Entry(root, width=50)
    url_entry.pack(padx=10, pady=5)

    scrape_button = tk.Button(root, text="Mulai Scraping", command=start_scraping)
    scrape_button.pack(pady=10)

    root.mainloop()

# ⛔ Hanya jalankan GUI jika file ini dieksekusi langsung
if __name__ == "__main__":
    run_gui()
