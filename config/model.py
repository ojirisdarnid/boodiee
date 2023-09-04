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