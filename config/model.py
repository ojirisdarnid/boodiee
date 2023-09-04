# Definisi kelas Item yang merepresentasikan barang dalam inventaris
class Item:
    def __init__(self, item_id, seller, theme, size, buy, sell, status):
        self.item_id = item_id
        self.seller = seller
        self.theme = theme
        self.size = size
        self.buy = buy
        self.sell = sell
        self.status = status