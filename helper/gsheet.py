import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Establish a connection to Google Spreadsheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("secret/boodiee-creds.json", scope) # Load the service account credentials from a JSON file
gc = gspread.authorize(creds) # Authorize the connection

spreadsheet = gc.open("boodiee") # Open a specific Google Spreadsheet by name
item_sheet = spreadsheet.worksheet("list_items") # Access specific worksheets within the spreadsheet
user_sheet = spreadsheet.worksheet("users") # Access specific worksheets within the spreadsheet
