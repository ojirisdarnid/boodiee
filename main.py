import os, sys
from loguru import logger
from dotenv import load_dotenv
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from service.command import *
from service.handler import *
from helper.log import *

# Load environment variables from secret/.env file
secret = 'secret/.env'
load_dotenv(dotenv_path=secret)
TOKEN = os.getenv("TOKEN")
        
# Fungsi utama untuk menjalankan bot
def main() -> None:
    logger.add(sink=sys.stdout, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    logger.add(log_file, rotation="10 MB", retention=retention, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    # Membuat objek Updater dengan menggunakan TOKEN bot
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, save_name)]
        },
        fallbacks=[]
    )

    # Menambahkan handler perintah sesuai dengan fungsinya
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    # dispatcher.add_handler(CommandHandler("add", command.add))
    # dispatcher.add_handler(CommandHandler("update", command.update))
    # dispatcher.add_handler(CommandHandler("delete", command.delete))
    # dispatcher.add_handler(CommandHandler("list", command.list))
    # dispatcher.add_handler(CallbackQueryHandler(command.inline_button_callback))
    
    # Memulai polling untuk mendapatkan update dari Telegram
    updater.start_polling()

    # Menjaga bot berjalan hingga dihentikan secara manual
    updater.idle()

# Memeriksa apakah skrip ini dijalankan sebagai program utama
if __name__ == "__main__":
    main()
