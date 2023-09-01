import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('boodiee-creds.json', scope)

# Authenticate and open the Google Sheet
gc = gspread.authorize(creds)
spreadsheet = gc.open("boodiee")
worksheet = spreadsheet.get_worksheet(0)  # Use the first worksheet

def get_next_item_id():
    # Get the next item ID from the Google Sheet
    next_item_id = worksheet.acell('A1').value
    return int(next_item_id)

def add_item(seller, theme, size, buy, sell, status):
    # Get the next item ID
    next_item_id = get_next_item_id()

    # Create a new row and add the item details
    new_row = [next_item_id, seller, theme, size, buy, sell, status]
    worksheet.append_table(new_row)  # Add a new row to the Google Sheet

    # Update the next item ID in the Google Sheet
    worksheet.update_acell('A1', str(next_item_id + 1))

    return next_item_id

# Add other functions as needed
