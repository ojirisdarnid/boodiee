import os
from datetime import datetime, timedelta

# Tentukan folder tempat Anda ingin menyimpan log
log_folder = "logs"

# Pastikan folder sudah ada atau buat jika belum ada
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Format nama file log dengan tanggal saat ini
log_file = os.path.join(log_folder, datetime.now().strftime("boodiee_%Y-%m-%d.log"))
retention = timedelta(days=3)