import logging, service, os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")
        
# Fungsi utama untuk menjalankan bot
def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    # Membuat objek Updater dengan menggunakan TOKEN bot
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    # Menambahkan handler perintah sesuai dengan fungsinya
    dispatcher.add_handler(CommandHandler("start", service.start))
    dispatcher.add_handler(CommandHandler("help", service.help))
    dispatcher.add_handler(CommandHandler("add", service.add))
    dispatcher.add_handler(CommandHandler("update", service.update))
    dispatcher.add_handler(CommandHandler("delete", service.delete))
    dispatcher.add_handler(CommandHandler("list", service.list))
    dispatcher.add_handler(CallbackQueryHandler(service.inline_button_callback))
    # New handler for the /start command
    dispatcher.add_handler(CommandHandler("start", service.start))
    # New handler to capture the user's name
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, service.text_handler))
    
    # Memulai polling untuk mendapatkan update dari Telegram
    updater.start_polling()

    # Menjaga bot berjalan hingga dihentikan secara manual
    updater.idle()

# Memeriksa apakah skrip ini dijalankan sebagai program utama
if __name__ == "__main__":
    main()
