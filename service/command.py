from service.handler import is_user_registered
from helper.gsheet import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, CallbackContext)
from loguru import logger

# Define constants, Constants used for indexing or identification purposes
NAME, CONFIRM_NAME = range(2)

# Function to start the bot
def start(update, context: CallbackContext):
    uname = update.message.from_user.username
    user_id = update.message.from_user.id
    logger.info(f"User {uname} initiated the /start command.")
# Check if the user already has a name in the list
    if is_user_registered(user_id):
        logger.info(f"User {uname} already in the list.")
        update.message.reply_text(f"You've already introduced yourself. You can use /help to see what i can help you with.")
    else:
        update.message.reply_text(f"Hi there! Welcome to Boodiee. I'm here to help you manage your inventory. To get started, could you please tell me your name?")
    return NAME

# Function to provide help and list available commands
def help(update: Update, context: CallbackContext) -> None:
    uname = update.message.from_user.username
    user_id = update.message.from_user.id
    logger.info(f"User {uname} initiated the /help command.")
# Check if user_id is not in the list
    if not is_user_registered(user_id):
        update.message.reply_text("Please register your name with /start before using this commands.")
    else:
        update.message.reply_text("Hello! I'm Boodiee, and I'm here to make your life easier. Need to keep track of things? No problem! Here's what I can assist you with :\n\n"
            "- To add items to your inventory, just use the command `/add`.\n"
            "- Curious about what's in your inventory? Type `/list` to see the whole list.\n"
            "- You can also use filter buttons in the `/list` to filter items by status (Ready, Sold, or PO).\n"
            "- If you want to update any item's details, the command you're looking for is `/update`.\n"
            "- Got something you no longer need? Let's tidy up with `/delete`.\n"
            "- Want to know your profit? Calculate it with `/profit`. You can view the profit data from sales in either the international market or the Indonesian market..\n\n"
            "Just let me know what you need, and I'll be at your service!")