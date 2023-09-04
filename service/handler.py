from loguru import logger
from helper.gsheet import *
from service.command import *
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

# Function to handle the seller's name input
def seller_name(update: Update, context: CallbackContext) -> int:
    context.user_data['seller'] = update.message.text
    update.message.reply_text("Thanks! Now, please provide the item's theme.")
    logger.info(f"User {update.message.from_user.username} provided seller name: {update.message.text}")

    return 1

# Function to handle the theme input
def theme(update: Update, context: CallbackContext) -> int:
    context.user_data['theme'] = update.message.text
    update.message.reply_text("Great! Now, please provide the item's size.")
    logger.info(f"User {update.message.from_user.username} provided item theme: {update.message.text}")

    return 2

# Function to handle the size input
def size(update: Update, context: CallbackContext) -> int:
    context.user_data['size'] = update.message.text
    update.message.reply_text("Got it! Please provide the stock quantity of the item.")
    logger.info(f"User {update.message.from_user.username} provided item size: {update.message.text}")

    return 3

# Function to handle the stock input
def stock(update: Update, context: CallbackContext) -> int:
    context.user_data['stock'] = update.message.text
    update.message.reply_text("Excellent! What is the buying price of the item?")
    logger.info(f"User {update.message.from_user.username} provided stock quantity: {update.message.text}")

    return 4

# Function to handle the buying price input
def buying_price(update: Update, context: CallbackContext) -> int:
    context.user_data['buying_price'] = update.message.text
    update.message.reply_text("Now, please provide the selling price of the item.")
    logger.info(f"User {update.message.from_user.username} provided buying price: {update.message.text}")

    return 5

# Function to handle the selling price input
def selling_price(update: Update, context: CallbackContext) -> int:
    context.user_data['selling_price'] = update.message.text
    update.message.reply_text("Almost there! Please specify the status of the item (e.g., 'Ready', 'Sold', 'PO').")
    logger.info(f"User {update.message.from_user.username} provided selling price: {update.message.text}")

    return 6

# Function to handle the status input
def status(update: Update, context: CallbackContext) -> int:
    context.user_data['status'] = update.message.text
    update.message.reply_text("Thanks! Will this item be listed on the International market? (Yes/No)")
    logger.info(f"User {update.message.from_user.username} provided item status: {update.message.text}")

    return 7

# Function to handle the "List on Market" question with inline keyboard
def list_on_market(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="yes"),
            InlineKeyboardButton("No", callback_data="no"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("Will this item be listed on the International market?", reply_markup=reply_markup)
    logger.info(f"User {update.message.from_user.username} asked if the item will be listed on the market.")

    return 7

# Callback function for handling inline keyboard button presses
def inline_button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    choice = query.data
    
    if choice == "yes":
        context.user_data['list_on_market'] = "yes"
        query.message.reply_text("Great! Please provide the selling price in $ for this item.")
        logger.info(f"User {query.from_user.username} chose to list the item on the market.")
        return 8
    elif choice == "no":
        context.user_data['list_on_market'] = "no"
        save_item_to_spreadsheet(context.user_data)
        query.message.reply_text("Item added to your inventory.")
        logger.info(f"User {query.from_user.username} chose not to list the item on the market.")
        return ConversationHandler.END

# Function to handle the selling price in dollars input
def selling_price_dollar(update: Update, context: CallbackContext) -> int:
    context.user_data['selling_price_dollar'] = update.message.text
    save_item_to_spreadsheet(context.user_data)
    update.message.reply_text("Item added to your inventory.")
    logger.info(f"User {update.message.from_user.username} provided selling price in dollars: {update.message.text}")

    return ConversationHandler.END

def save_item_to_spreadsheet(data, item_id):
    row = [
        item_id,  # Menyimpan ID item
        data['seller'],
        data['theme'],
        data['size'],
        data['stock'],
        data['buying_price'],
        data['selling_price'],
        data['selling_price_dollar'],
        data['status'],
        data['list_on_market'],
    ]
    item_sheet.insert_row(row)
    logger.info(f"Item data saved to spreadsheet with ID: {item_id}")