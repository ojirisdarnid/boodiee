import os, sys
from loguru import logger
from dotenv import load_dotenv
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from service.command import start, help, add
from service.handler import save_name, seller_name, theme, size, stock, buying_price, selling_price, status,list_on_market, selling_price_dollar, inline_button
from helper.log import *

# Load environment variables from secret/.env file
secret = 'secret/.env'
load_dotenv(dotenv_path=secret)
TOKEN = os.getenv("TOKEN")
        
# Main Function for running bot
def main() -> None:
    logger.info("Starting the bot")
    logger.add(sink=sys.stdout, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    logger.add(log_file, rotation="10 MB", retention=retention, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    
    # Membuat objek Updater dengan menggunakan TOKEN bot
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, save_name)]
        },
        fallbacks=[]
    )

    # Adding the conversation handler for /add command
    add_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            0: [MessageHandler(Filters.text & ~Filters.command, seller_name)],
            1: [MessageHandler(Filters.text & ~Filters.command, theme)],
            2: [MessageHandler(Filters.text & ~Filters.command, size)],
            3: [MessageHandler(Filters.text & ~Filters.command, stock)],
            4: [MessageHandler(Filters.text & ~Filters.command, buying_price)],
            5: [MessageHandler(Filters.text & ~Filters.command, selling_price)],
            6: [MessageHandler(Filters.text & ~Filters.command, status)],
            7: [MessageHandler(Filters.text & ~Filters.command, list_on_market)],
            8: [MessageHandler(Filters.text & ~Filters.command, selling_price_dollar)],
        },
        fallbacks=[],
    )
    
    # Menambahkan handler perintah sesuai dengan fungsinya
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(add_conv_handler)
    # dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    # dispatcher.add_handler(CommandHandler("add", add))
    # dispatcher.add_handler(CommandHandler("update", command.update))
    # dispatcher.add_handler(CommandHandler("delete", command.delete))
    # dispatcher.add_handler(CommandHandler("list", command.list))
    # Adding a CallbackQueryHandler for inline button handling
    dispatcher.add_handler(CallbackQueryHandler(inline_button))
    
    # Memulai polling untuk mendapatkan update dari Telegram
    updater.start_polling()

    # Menjaga bot berjalan hingga dihentikan secara manual
    updater.idle()

# Memeriksa apakah skrip ini dijalankan sebagai program utama
if __name__ == "__main__":
    main()
