import os
import requests
import tkinter as tk
from tkinter import messagebox, ttk
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../website/novels/"))

def save_container_html(h1_title, content_html, folder_path, filename='index.html'):
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{h1_title}</title>
    <link rel="stylesheet" href="../../src/style-novel.css">
    <script src="../../js/jquery.js"></script>
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
            <button id="stop-scroll" class="scroll-button stop" disabled>Henti</button>
            <button id="fullscreen-button" class="scroll-button fullscreen">Fullscreen</button>
            <form action="../" target="_blank" style="display: inline;">
                <button type="submit" class="scroll-button temp-button">T</button>
            </form>        
        </div>
    </div>
    <h1>{h1_title}</h1>
    <aside class="vertical-aside">{h1_title}</aside>
    {content_html}
    <script src="../../js/autoscroll.js"></script>
    <script src="../../js/fullscreen.js"></script>
</body>
</html>
"""
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"[SAVED] {file_path}")

def scrape_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        print(f"[ERROR] Gagal fetch: {url} | {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    h1_title = "Chapter"
    epheader = soup.find('div', class_='epheader')
    if epheader:
        h1 = epheader.find('h1')
        if h1:
            h1_title = h1.get_text(strip=True)

    content_div = soup.find('div', class_='text-left')
    if not content_div:
        print(f"[WARNING] Konten tidak ditemukan di: {url}")
        return

    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.strip()
        valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        folder_name = ''.join(c for c in title if c in valid_chars).replace(" ", "_")
    else:
        folder_name = url.strip('/').split('/')[-1]

    folder_path = os.path.join(SAVE_BASE_DIR, folder_name)
    save_container_html(h1_title, str(content_div), folder_path)

def run_gui():
    def start_scraping():
        txt_file = file_var.get()
        if not txt_file:
            messagebox.showwarning("Peringatan", "Pilih file .txt terlebih dahulu!")
            return

        try:
            start_line = int(start_entry.get())
            end_line = int(end_entry.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Masukkan angka yang valid.")
            return

        txt_path = os.path.join(SCRIPT_DIR, txt_file)
        if not os.path.exists(txt_path):
            messagebox.showerror("File Tidak Ditemukan", f"{txt_file} tidak ditemukan.")
            return

        with open(txt_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
            selected_urls = urls[start_line - 1:end_line]

        for url in selected_urls:
            print(f"[SCRAPE] {url}")
            scrape_url(url)

        messagebox.showinfo("Selesai", "Scraping selesai!")

    def refresh_txt_files():
        txt_files = [f for f in os.listdir(SCRIPT_DIR) if f.endswith(".txt")]
        file_menu['values'] = txt_files
        if txt_files:
            file_var.set(txt_files[0])

    # GUI Setup
    root = tk.Tk()
    root.title("Novel Scraper dari File TXT")

    tk.Label(root, text="Pilih File .txt:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    file_var = tk.StringVar()
    file_menu = ttk.Combobox(root, textvariable=file_var, width=50)
    file_menu.grid(row=0, column=1, padx=10, pady=5)
    refresh_txt_files()

    tk.Label(root, text="Baris mulai (chapter):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    start_entry = tk.Entry(root, width=10)
    start_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="Baris akhir (chapter):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    end_entry = tk.Entry(root, width=10)
    end_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    scrape_button = tk.Button(root, text="Mulai Scraping", command=start_scraping)
    scrape_button.grid(row=3, column=0, columnspan=2, pady=15)

    root.mainloop()

if __name__ == "__main__":
    run_gui()