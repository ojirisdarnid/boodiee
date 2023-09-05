import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Establish a connection to Google Spreadsheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("secret/boodiee-creds.json", scope) # Load the service account credentials from a JSON file
gc = gspread.authorize(creds) # Authorize the connection

spreadsheet = gc.open("boodiee") # Open a specific Google Spreadsheet by name
item_sheet = spreadsheet.worksheet("list_items") # Access specific worksheets within the spreadsheet
user_sheet = spreadsheet.worksheet("users") # Access specific worksheets within the spreadsheet

# Mencari baris kosong di kolom A
cell_list = item_sheet.findall("", in_column=1)
if cell_list:
    first_empty_row = cell_list[0].row
else:
    # Jika tidak ada baris kosong, tambahkan di akhir spreadsheet
    first_empty_row = len(item_sheet.get_all_records()) + 2  # +2 karena header dan mulai dari baris 2