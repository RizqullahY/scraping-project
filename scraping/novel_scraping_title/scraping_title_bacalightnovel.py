import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def scrape(url, ambil_pdf):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ambil judul halaman sebagai nama file
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text.strip()
            valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            safe_title = ''.join(c for c in title if c in valid_chars).replace(' ', '_')
        else:
            safe_title = "output"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(current_dir, f"{safe_title}.txt")

        # Temukan semua elemen <li> yang punya data-ID
        list_items = soup.find_all('li', attrs={'data-id': True})

        urls = []
        for li in list_items:
            if ambil_pdf:
                # Ambil link PDF
                link_tag = li.find('a', class_='dlpdf')
            else:
                # Ambil link utama ke halaman chapter
                link_tag = li.find('a', href=True)

            if link_tag and 'href' in link_tag.attrs:
                full_url = link_tag['href']
                urls.append(full_url)

        urls.reverse()

        with open(output_file, 'w', encoding='utf-8') as f:
            for link in urls:
                f.write(f"{link}\n")

        messagebox.showinfo("Berhasil", f"Hasil disimpan ke:\n{output_file}")
    else:
        messagebox.showerror("Gagal", f"Status code: {response.status_code}")

def run_gui():
    def start_scraping():
        url = url_entry.get().strip()
        if not url:
            messagebox.showwarning("Peringatan", "URL tidak boleh kosong!")
            return
        ambil_pdf = pdf_var.get()
        scrape(url, ambil_pdf)

    # GUI setup
    root = tk.Tk()
    root.title("BacaLightNovel Scraper")

    tk.Label(root, text="Masukkan URL Novel:").pack(padx=10, pady=(10, 2))

    url_entry = tk.Entry(root, width=50)
    url_entry.pack(padx=10, pady=5)

    pdf_var = tk.BooleanVar()
    pdf_checkbox = tk.Checkbutton(root, text="Ambil versi PDF", variable=pdf_var)
    pdf_checkbox.pack()

    scrape_button = tk.Button(root, text="Mulai Scraping", command=start_scraping)
    scrape_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    run_gui()