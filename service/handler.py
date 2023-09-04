from loguru import logger
from helper.gsheet import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, CallbackContext)

# Function to save the user's name to the spreadsheet
def save_name(update, context: CallbackContext):
    uname = update.message.from_user.username
    user = update.message.from_user
    name = update.message.text

# Check if the user already has a name in the list
    if is_user_registered(user.id):
        update.message.reply_text(f"You've already introduced yourself. You can use /help to see what i can help you with.")
        return ConversationHandler.END
# Check if the name has a minimum of 3 characters
    if len(name) < 3:
        logger.info(f"User {uname} entered a name that is to short.")
        update.message.reply_text(f"Name must be at least 3 characters long. Please enter a valid name :")
    else:
        user_sheet.insert_row([user.id, uname, name], 2)
        logger.info(f"User {uname} entered a correct name format. Name writes in the {user_sheet}")
        update.message.reply_text(f"Nice to meet you, {name}! You can now use the bot, use /help to see what i can help you with.")
        return ConversationHandler.END

# Function to check if the user is registered
def is_user_registered(user_id):
    user_ids = user_sheet.col_values(1)
    return str(user_id) in user_ids