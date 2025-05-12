# 🕷️ Scraping App - Desktop GUI

Proyek ini merupakan aplikasi desktop berbasis **Tkinter** untuk scraping data dari berbagai sumber (komik, novel, dll), dikemas menjadi file `.exe` menggunakan **PyInstaller**.

---

## 📁 Struktur Folder

```bash
project_root/
├── scraping/
│   ├── comic_scraping_image/
│   ├── comic_scraping_title/
│   ├── novel_scraping_content/
│   ├── novel_scraping_title/
│   ├── __init__.py
│   ├── main.py                # GUI utama
│   ├── scraper_registry.py    # Registrasi semua fitur scraping
├── dist/                      # Hasil akhir .exe akan muncul di sini
├── build/
├── main.spec
```

---

## ⚙️ Setup Virtual Environment

1. **Buat virtual environment (opsional tapi direkomendasikan)**

```bash
virtualenv .
```

2. **Aktifkan virtual environment**

* Windows:

  ```bash
  .\Scripts\activate
  ```

* macOS/Linux:

  ```bash
  source bin/activate
  ```

3. **Install semua dependensi**

Pastikan kamu sudah menginstall paket yang dibutuhkan seperti:

```bash
pip install requests beautifulsoup4 pyinstaller
```

---

## 🛠️ Build Menjadi .exe

### Langkah 1: Compile awal

```bash
pyinstaller --noconsole --onefile scraping/main.py
```

Langkah ini akan menghasilkan `main.spec`. Kita akan edit file itu untuk menyertakan file tambahan.

---

### Langkah 2: Edit `main.spec`

Tambahkan bagian berikut di dalam argument `Analysis(...)`:

```python
datas=[
    ('scraping/scraper_registry.py', 'scraping'),
],
```

Contoh (cuplikan):

```python
a = Analysis(
    ['scraping/main.py'],
    ...
    datas=[('scraping/scraper_registry.py', 'scraping')],
    ...
)
```

---

### Langkah 3: Build ulang dengan .spec

```bash
pyinstaller main.spec
```

Setelah selesai, file `.exe` akan muncul di dalam folder `dist/`.

---

## 🔧 Jika Terjadi Error `ModuleNotFoundError`

Pastikan di dalam `main.py`:

✅ Gunakan **import relatif yang benar**, karena `main.py` ada di dalam folder `scraping`:

```python
from scraping.scraper_registry import scrapers
```

⛔ **Jangan** tulis:

```python
from scraper_registry import scrapers  # ❌ Salah
```

---

## ✅ Tips Tambahan

* Gunakan `--noconsole` agar jendela terminal tidak muncul saat menjalankan GUI.
* Pastikan semua file `.py` sudah dikenali sebagai modul Python dengan menambahkan `__init__.py` di dalam setiap folder.

---

## 🧪 Jalankan Aplikasi

Setelah build berhasil:

```bash
dist\main.exe  # Windows
```

Atau klik langsung file `.exe` di `dist/`.


![pexels-eberhardgross-1421903 (1)](https://github.com/user-attachments/assets/8727addd-b787-40bb-865e-ee324ed3e8f5)
