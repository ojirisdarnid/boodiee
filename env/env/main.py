from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging

TOKEN = "6682175888:AAH-ysOL5L-3U3pJsgU5b3FvFQX8gKIKxJM"

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

next_item_id = 1
available_item_ids = set()
inventory = {}

# Fungsi untuk /help
def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm Boodiee, and I'm here to make your life easier. Need to keep track of things? No problem! Here's what I can assist you with:\n\n"
        "- To add items to your inventory, just use the command `/add`.\n"
        "- Curious about what's in your inventory? Type `/list` to see the whole list.\n"
        "- If you want to update any item's details, the command you're looking for is `/update`.\n"
        "- Got something you no longer need? Let's tidy up with `/delete`.\n\n"
        "Just let me know what you need, and I'll be at your service!")
    
# Fungsi untuk /add
def add(update: Update, context: CallbackContext) -> None:
    global next_item_id  
    # print("Add item function called.")   
    user_id = update.message.from_user.id
    params = update.message.text.replace("/add ", "").split(",")    
    # print("Params:", params)
    # Memeriksa apakah jumlah parameter sesuai dengan yang diharapkan
    if len(params) != 6:
        update.message.reply_text("Format: /add Seller, Theme, Size, Buying Price, Selling Price, Status")
        return    
    seller, theme, size, buy, sell, status = params
    # Mengecek apakah pengguna memiliki inventaris atau belum  
    if user_id not in inventory:
        inventory[user_id] = []
        
    if available_item_ids:
        item_id = available_item_ids.pop()
    else:
        item_id = next_item_id
        next_item_id += 1
        
    # Membuat objek Item baru dan menambahkannya ke inventaris pengguna
    item = Item(item_id, seller, theme, size, buy, sell, status)
    inventory[user_id].append(item)    
    # print("Item added with ID:", next_item_id)     
    update.message.reply_text(f"Item '{item.theme}' has been added to your inventory.")

# Fungsi /update
def update(update: Update, context: CallbackContext) -> None:
    # Mendapatkan ID pengguna yang mengirim pesan kepada bot
    user_id = update.message.from_user.id   
    # Memecah pesan menjadi parameter menggunakan "/update " dan , sebagai pemisah, lalu dimasukkan ke dalam daftar "params"
    params = update.message.text.replace("/update ", "").split(",")    
    # Memeriksa apakah jumlah parameter sesuai dengan yang diharapkan (yaitu 3)
    if len(params) != 3:
        update.message.reply_text("Format: /update Number, Field_to_update, New_value")
        return   
    # Memisahkan nilai dari parameter ke variabel "number", "field_to_update", dan "new_value"
    number, field_to_update, new_value = params    
    # Memeriksa apakah pengguna memiliki inventaris dan inventaris tidak kosong
    if user_id in inventory and inventory[user_id]:
        updated = False
        # Melakukan loop melalui item-item dalam inventaris pengguna
        for item in inventory[user_id]:
            print("Field to update:", field_to_update)
            # Memeriksa apakah nomor item cocok dengan nomor yang diberikan dalam perintah
            if item.item_id == int(number):
                # Memeriksa field mana yang akan diperbarui
                if field_to_update == " seller":
                    item.seller = new_value
                elif field_to_update == " theme":
                    item.theme = new_value
                elif field_to_update == " size":
                    item.size = new_value
                elif field_to_update == " buy":
                    item.buy = new_value
                elif field_to_update == " sell":
                    item.sell = new_value
                elif field_to_update == " status":
                    item.status = new_value
                else:
                    update.message.reply_text("Invalid field name. Allowed fields: seller, theme, size, buy, sell, status")
                    return               
                # Mengirimkan pesan balasan bahwa field dari item telah diperbarui
                update.message.reply_text(f"Field '{field_to_update}' of item '{item.theme}' has been updated.")
                updated = True
                break        
        # Jika item tidak ditemukan dalam inventaris
        if not updated:
            update.message.reply_text(f"Item with number '{number}' not found in your inventory.")
    else:
        update.message.reply_text("Your Inventory is Empty. Add an item first using /add .")

# Fungsi /delete
def delete(update: Update, context: CallbackContext) -> None:
    # Mendapatkan ID pengguna yang mengirim pesan kepada bot
    user_id = update.message.from_user.id
    # Memperoleh nomer item yang akan dihapus dari pesan yang dikirim pengguna
    number = update.message.text.replace("/delete ", "")

    # Memeriksa apakah pengguna memiliki inventaris dan inventaris tidak kosong
    if user_id in inventory and inventory[user_id]:
        # Melakukan loop melalui item-item dalam invetaris pengguna
        for item in inventory[user_id]:
            # Memeriksa apakah nomer item yang ada dalam inventory cocok dengan nomer yang dikirim oleh pengguna
            if str(item.item_id) == number:
                available_item_ids.add(item.item_id)
                # Menghapus item dari inventaris
                inventory[user_id].remove(item)
                update.message.reply_text(f"Item '{item.theme}' has been delete from your inventory.")
                break
            
        else:
            # Jika nomer yang dikirim oleh pengguna tidak ditemukan di dalam inventory atau tidak cocok    
            update.message.reply_text(f"Item with number '{number}' not found in your inventory, please check the list again.")
    else:
        update.message.reply_text(f"Your Inventory is Empty. Add an item first using /add .")
    
    # # Mereset counter next_item_id untuk pengguna jika seluruh item dihapus
    # if user_id in inventory and len(inventory[user_id]) == 0:
    #     next_item_id[user_id] = 1
            
# Fungsi /list
def list(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    logging.info(f"Received /list command from user {user_id}")
    
    # Memeriksa apakah pengguna memiliki inventaris dan inventaris tidak kosong    
    if user_id in inventory and inventory[user_id]:
        sorted_item = sorted(inventory[user_id], key=lambda item: item.item_id)
        items_info = []
        for item in sorted_item:
            item_info = (
                f"Number: {item.item_id}\n"
                f"Seller: {item.seller}\n"
                f"Theme: {item.theme}\n"
                f"Size: {item.size}\n"
                f"Buying Price: {item.buy}\n"
                f"Selling Price: {item.sell}\n"
                f"Status: {item.status}\n"
            )
            items_info.append(item_info)
        
        all_items = "\n\n".join(items_info)

        keyboard = [
            [InlineKeyboardButton("Ready", callback_data="status_Ready"),
             InlineKeyboardButton("Sold", callback_data="status_Sold"),
             InlineKeyboardButton("PO", callback_data="status_PO")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(f"Your Inventory :\n\n{all_items}\n\nSelect a status:", reply_markup=reply_markup)
    else:
        update.message.reply_text("Your Inventory is Empty. Add an item now using /add .")

# ...

# Callback function for inline buttons
def inline_button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    status_callback = query.data.replace("status_", " ")  # Extract the status from the callback_data
    
    print("User ID:", user_id)
    print("Status Callback:", status_callback)
    
    if user_id in inventory and inventory[user_id]:
        print("Inventory for User:", inventory[user_id])
        filtered_items = [item for item in inventory[user_id] if item.status == status_callback]
        print("Filtered Items:", filtered_items)
        if filtered_items:
            items_info = []

            for item in filtered_items:
                item_info = (
                    f"Number: {item.item_id}\n"
                    f"Seller: {item.seller}\n"
                    f"Theme: {item.theme}\n"
                    f"Size: {item.size}\n"
                    f"Buying Price: {item.buy}\n"
                    f"Selling Price: {item.sell}\n"
                    f"Status: {item.status}\n"
                )
                items_info.append(item_info)

            all_items = "\n\n".join(items_info)
            query.message.reply_text(f"Items with status '{status_callback.capitalize()}':\n{all_items}")
        else:
            query.message.reply_text(f"No items found with status '{status_callback.capitalize()}'.")
    else:
        query.message.reply_text("Your Inventory is Empty. Add an item now using /add .")
        
# Fungsi utama untuk menjalankan bot
def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    # Membuat objek Updater dengan menggunakan TOKEN bot
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    # Menambahkan handler perintah sesuai dengan fungsinya
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("update", update))
    dispatcher.add_handler(CommandHandler("delete", delete))
    dispatcher.add_handler(CommandHandler("list", list))
    dispatcher.add_handler(CallbackQueryHandler(inline_button_callback))

    
    # Memulai polling untuk mendapatkan update dari Telegram
    updater.start_polling()

    # Menjaga bot berjalan hingga dihentikan secara manual
    updater.idle()

# Memeriksa apakah skrip ini dijalankan sebagai program utama
if __name__ == "__main__":
    main()
