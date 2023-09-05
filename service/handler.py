from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, CallbackContext)
from telegram.parsemode import ParseMode
from loguru import logger
from helper.gsheet import user_sheet, item_sheet, first_empty_row
from config.base import ConversationConstant
from helper.utils import item_id

# Function to save the user's name to the spreadsheet
def save_name(update, context: CallbackContext):
    uname = update.message.from_user.username
    user = update.message.from_user
    name = update.message.text

# Check if the user already has a name in the list
    if is_user_registered(user.id):
        logger.info(f"User {uname} already in the list.")
        update.message.reply_text(f"You've already introduced yourself `{user.first_name}`. Use /help to see what i can help you with.", parse_mode=ParseMode.MARKDOWN)
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
    logger.info(f"User {update.message.from_user.username} provided seller name : {update.message.text}")

    return ConversationConstant.THEME

# Function to handle the theme input
def theme(update: Update, context: CallbackContext) -> int:
    context.user_data['theme'] = update.message.text
    update.message.reply_text("Great! Now, please provide the item's size.")
    logger.info(f"User {update.message.from_user.username} provided item theme : {update.message.text}")

    return ConversationConstant.SIZE

# Function to handle the size input
def size(update: Update, context: CallbackContext) -> int:
    context.user_data['size'] = update.message.text
    update.message.reply_text("Got it! Please provide the stock quantity of the item.")
    logger.info(f"User {update.message.from_user.username} provided item size : {update.message.text}")

    return ConversationConstant.STOCK

# Function to handle the stock input
def stock(update: Update, context: CallbackContext) -> int:
    context.user_data['stock'] = update.message.text
    update.message.reply_text("Excellent! What is the buying price of the item?")
    logger.info(f"User {update.message.from_user.username} provided stock quantity : {update.message.text}")

    return ConversationConstant.BUYING_PRICE

# Function to handle the buying price input
def buying_price(update: Update, context: CallbackContext) -> int:
    context.user_data['buying_price'] = update.message.text
    update.message.reply_text("Now, please provide the selling price of the item.")
    logger.info(f"User {update.message.from_user.username} provided buying price : {update.message.text}")

    return ConversationConstant.SELLING_PRICE

# Function to handle input for item selling price and show inline buttons for item status
def selling_price(update, context):
    user_id = update.message.from_user.id
    selling_price = update.message.text
    logger.info(f"User {update.message.from_user.username} provided selling price : {update.message.text}")
    context.user_data['selling_price'] = selling_price

    keyboard = [
        [InlineKeyboardButton("Ready", callback_data='Ready'),
         InlineKeyboardButton("Sold", callback_data='Sold'),
         InlineKeyboardButton("PO", callback_data='PO')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please select status of the item :", reply_markup=reply_markup)
    return ConversationConstant.INLINE_BUTTON

# Function to handle inline button selection for item status
def inline_button(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    status = query.data
    context.user_data['status'] = status
    logger.info(f"{status}")

    if status == 'PO':
        update.callback_query.answer()
        logger.info(f"{context.user_data}")
        context.user_data['list_on_market'] = 'No'
        context.user_data['selling_price_dollar'] = '-'
        save_item_to_spreadsheet(context.user_data, item_id)
        update.callback_query.message.reply_text("Item saved in inventory.")
        logger.info(f"Item from user {query.from_user.username} still in {status} status.")
        return ConversationHandler.END
    else:
        update.callback_query.answer()
        logger.info(f"Item from user {query.from_user.username} is {status}.")
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data='Yes'),
             InlineKeyboardButton("No", callback_data='No')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text("Do you want to list the item on the international market?", reply_markup=reply_markup)
        return ConversationConstant.LIST_ON_MARKET
    
# Function to handle inline button selection for listing on international market
def list_on_market(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    choice = query.data
    context.user_data['list_on_market'] = choice

    if choice == 'Yes':
        update.callback_query.answer()
        update.callback_query.message.reply_text("Great! Please provide the selling price in $ for this item.")
        logger.info(f"User {query.from_user.username} choose to list the item on the market.")
        return ConversationConstant.SELLING_PRICE_DOLLAR
    else:
        update.callback_query.answer()
        context.user_data['selling_price_dollar'] = '-'
        logger.info(f"{context.user_data}")
        save_item_to_spreadsheet(context.user_data, item_id)
        update.callback_query.message.reply_text("Item saved in inventory.")
        logger.info(f"User {query.from_user.username} choose not to list the item on the market.")
        return ConversationHandler.END
    
# Function to handle the selling price in dollars input
def selling_price_dollar(update: Update, context: CallbackContext) -> int:
    context.user_data['selling_price_dollar'] = update.message.text
    logger.info(f"{context.user_data}")
    logger.info(f"User {update.message.from_user.username} provided selling price ${update.message.text}")
    save_item_to_spreadsheet(context.user_data, item_id)
    update.message.reply_text("Item added to your inventory.")
    logger.info(f"User {update.message.from_user.username} provided selling price is ${update.message.text}")

    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("Item listing process canceled.")
    USER_DATA.pop(update.message.from_user.id, None)
    return ConversationHandler.END

def save_item_to_spreadsheet(data, item_id):
    # Pastikan data yang dibutuhkan ada di dalam context.user_data
    if 'seller' in data and 'theme' in data and 'size' in data and 'stock' in data and 'buying_price' in data and 'selling_price' in data:
        row = [
            item_id, 
            data['seller'],
            data['theme'],
            data['size'],
            data['stock'],
            data['buying_price'],
            data['selling_price'],
            data['status'],
            data['list_on_market'],
            data['selling_price_dollar'],  # Menggunakan get() untuk mendapatkan data dengan aman jika tidak ada          
        ]
        item_sheet.insert_row(row, first_empty_row)
        logger.info(f"Item data saved to spreadsheet with ID: {item_id}")  # Anda bisa menggunakan 'seller' atau 'item_id' sesuai kebutuhan
    else:
        logger.error("Incomplete data provided to save_item_to_spreadsheet")
