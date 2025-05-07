import os
import time
import requests
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../views/comic-image"))

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
            time.sleep(3)
    print(f"Failed to download {img_url} after {retries} attempts.")

def scrape_images_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img', itemprop='image')
        image_urls = [img['src'] for img in images if 'src' in img.attrs]

        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text.strip()
            valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            folder_name = ''.join(c for c in title if c in valid_chars).replace(' ', '_')
        else:
            folder_name = url.strip('/').split('/')[-1]

        folder_path = os.path.join(SAVE_BASE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        index_source = os.path.join(SCRIPT_DIR, 'index.html')
        index_dest = os.path.join(folder_path, 'index.html')
        try:
            shutil.copy(index_source, index_dest)
        except FileNotFoundError:
            print("index.html tidak ditemukan!")

        for i, img_url in enumerate(image_urls, start=1):
            img_path = os.path.join(folder_path, f"image_{i}.jpg")
            download_image(img_url, img_path)
    else:
        print(f"Failed to fetch page {url}, status code: {response.status_code}")

def start_scraping():
    txt_file = file_var.get()
    if not txt_file:
        messagebox.showwarning("Peringatan", "Pilih file .txt terlebih dahulu!")
        return

    try:
        start_line = int(start_entry.get())
        end_line = int(end_entry.get())
    except ValueError:
        messagebox.showwarning("Input Error", "Masukkan angka yang valid untuk range.")
        return

    txt_path = os.path.join(SCRIPT_DIR, txt_file)
    if not os.path.exists(txt_path):
        messagebox.showerror("File Tidak Ditemukan", f"{txt_file} tidak ditemukan.")
        return

    with open(txt_path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
        selected_urls = urls[start_line - 1:end_line]

    for chapter_url in selected_urls:
        print(f"Scraping: {chapter_url}")
        scrape_images_from_url(chapter_url)

    messagebox.showinfo("Selesai", "Scraping selesai!")

def refresh_txt_files():
    txt_files = [f for f in os.listdir(SCRIPT_DIR) if f.endswith(".txt")]
    file_menu['values'] = txt_files
    if txt_files:
        file_var.set(txt_files[0])

# GUI Setup
root = tk.Tk()
root.title("Komik Image Scraper")

tk.Label(root, text="Pilih File .txt:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
file_var = tk.StringVar()
file_menu = ttk.Combobox(root, textvariable=file_var, width=50)
file_menu.grid(row=0, column=1, padx=10, pady=5)
refresh_txt_files()

tk.Label(root, text="Chapter mulai (baris):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
start_entry = tk.Entry(root, width=10)
start_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Chapter akhir (baris):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
end_entry = tk.Entry(root, width=10)
end_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

start_button = tk.Button(root, text="Mulai Scraping", command=start_scraping)
start_button.grid(row=3, column=0, columnspan=2, pady=15)

root.mainloop()
