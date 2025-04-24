import os

# Ambil path direktori saat ini
current_dir = os.path.dirname(os.path.abspath(__file__))

# Nama file output
output_file = os.path.join(current_dir, "for-web-v1.txt")

# Buka file untuk menulis
with open(output_file, "w") as f:
    for i in range(1, 201):
        img_tag = f'''<img
  src="./image/image_{i}.jpg"
  alt="Sudah Habis Atau Sudah Tau Kalau Error"
/>\n'''
        f.write(img_tag)

print(f"File berhasil dibuat di: {output_file}")
