import os, random, string
from datetime import datetime, timedelta

# Inisialisasi set untuk melacak item_id yang telah digunakan
used_item_ids = set()

def get_unique_item_id():
    while True:
        # Memilih dua huruf acak dari string.ascii_letters
        letters = ''.join(random.choice(string.ascii_letters) for _ in range(2))
        # Memilih tiga angka acak dari string.digits
        digits = ''.join(random.choice(string.digits) for _ in range(2))
        # Menggabungkan huruf dan angka
        item_id = letters.lower() + digits
        if item_id not in used_item_ids:
            used_item_ids.add(item_id)
            return item_id

# Penggunaan:
item_id = get_unique_item_id()
# Tentukan folder tempat Anda ingin menyimpan log
log_folder = "logs"

# Pastikan folder sudah ada atau buat jika belum ada
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Format nama file log dengan tanggal saat ini
log_file = os.path.join(log_folder, datetime.now().strftime("boodiee_%Y-%m-%d.log"))
retention = timedelta(days=3)