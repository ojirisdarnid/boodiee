import os
from dotenv import load_dotenv

# Load environment variables from secret/.env file
secret = 'secret/.env'
load_dotenv(dotenv_path=secret)
TOKEN = os.getenv("TOKEN")

# Define class for constants, Constants used for identification user name
class StartConstant:
    NAME = range(1)
    
# Defining constants for conversation
class ConversationConstant:
    SELLER, THEME, SIZE, STOCK, BUYING_PRICE, SELLING_PRICE, INLINE_BUTTON, LIST_ON_MARKET, SELLING_PRICE_DOLLAR = range(9)

# Definisi kelas Item yang merepresentasikan barang dalam inventaris
class Item:
    def __init__(self, item_id, seller, theme, stock, size, buy, sell, status, int_market, in_dollar):
        self.item_id = item_id
        self.seller = seller
        self.theme = theme
        self.stock = stock
        self.size = size
        self.buy = buy
        self.sell = sell
        self.status = status
        self.int_market = int_market
        self.in_dollar = in_dollar