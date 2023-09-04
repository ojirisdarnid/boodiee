from service.handler import is_user_registered
from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from loguru import logger
import uuid

# Create unique ID for new item
item_id = str(uuid.uuid4())
# Define constants, Constants used for indexing or identification purposes
NAME, CONFIRM_NAME = range(2)
# Defining constants for conversation
SELLER, THEME, SIZE, STOCK, BUYING_PRICE, SELLING_PRICE, STATUS, LIST_ON_MARKET, SELLING_PRICE_DOLLAR = range(9)

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
        update.message.reply_text("Please register your name with /start before using this command.")
    else:
        update.message.reply_text("Hello! I'm Boodiee, and I'm here to make your life easier. Need to keep track of things? No problem! Here's what I can assist you with :\n\n"
            "- To add items to your inventory, just use the command `/add`.\n"
            "- Curious about what's in your inventory? Type `/list` to see the whole list.\n"
            "- You can also use filter buttons in the `/list` to filter items by status (Ready, Sold, or PO).\n"
            "- If you want to update any item's details, the command you're looking for is `/update`.\n"
            "- Got something you no longer need? Let's tidy up with `/delete`.\n"
            "- Want to know your profit? Calculate it with `/profit`. You can view the profit data from sales in either the international market or the Indonesian market..\n\n"
            "Just let me know what you need, and I'll be at your service!")
        
# Function to add new item to list
def add(update: Update, context: CallbackContext) -> None:
    uname = update.message.from_user.username
    user_id = update.message.from_user.id
    logger.info(f"User {uname} initiated the /add command.")
    
    if not is_user_registered(user_id):
        update.message.reply_text("Please register your name with /start before using this command.")
        return ConversationHandler.END

    # Generate a unique item ID using UUID
    item_id = str(uuid.uuid4())
    context.user_data['item_id'] = item_id  

    # Reset all item data fields
    context.user_data['seller'] = ""
    context.user_data['theme'] = ""
    context.user_data['size'] = ""
    context.user_data['stock'] = ""
    context.user_data['buying_price'] = ""
    context.user_data['selling_price'] = ""
    context.user_data['selling_price_dollar'] = ""
    context.user_data['status'] = ""

    update.message.reply_text("Great! Let's start adding a new item to your inventory.")
    update.message.reply_text("First, please provide the seller's name.")
    
    return 0