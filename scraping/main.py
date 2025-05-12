import tkinter as tk
from tkinter import messagebox
import sys
import os


# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraping.scraper_registry import scrapers

def run_scraper():
    category = selected_category.get()
    feature = selected_feature.get()
    func = scrapers.get(category, {}).get(feature)
    if func:
        try:
            func()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Fitur belum ditemukan.")

def update_features(*args):
    category = selected_category.get()
    features = list(scrapers.get(category, {}).keys())
    selected_feature.set(features[0] if features else "")
    menu = feature_menu["menu"]
    menu.delete(0, "end")
    for feat in features:
        menu.add_command(label=feat, command=lambda value=feat: selected_feature.set(value))

# GUI Setup
root = tk.Tk()
root.title("Scraping App")
root.geometry("300x250")

# Kategori Dropdown
tk.Label(root, text="Pilih Kategori:").pack(pady=(10, 0))
selected_category = tk.StringVar()
selected_category.trace_add("write", update_features)
category_menu = tk.OptionMenu(root, selected_category, *scrapers.keys())
category_menu.config(width=25) 
category_menu.pack(pady=5)

# Fitur Dropdown
tk.Label(root, text="Pilih Fitur:").pack(pady=(10, 0))
selected_feature = tk.StringVar()
feature_menu = tk.OptionMenu(root, selected_feature, "")
feature_menu.config(width=25) 
feature_menu.pack(pady=5)

# Tombol Jalankan
tk.Button(root, text="Jalankan", command=run_scraper).pack(pady=20)

# Set default saat start
if scrapers:
    default_category = next(iter(scrapers))
    selected_category.set(default_category)

root.mainloop()
