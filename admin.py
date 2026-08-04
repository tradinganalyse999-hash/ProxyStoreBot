from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_buttons():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("➕ Add Balance", callback_data="admin_add_balance"))
    markup.add(InlineKeyboardButton("📦 All Orders", callback_data="admin_orders"))
    markup.add(InlineKeyboardButton("⏳ Pending Orders", callback_data="admin_pending"))
    return markup