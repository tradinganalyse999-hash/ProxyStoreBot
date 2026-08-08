from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ Add Balance", callback_data="admin_add_balance"),
        InlineKeyboardButton("📦 All Orders", callback_data="admin_orders")
    )
    markup.add(
        InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
        InlineKeyboardButton("📦 Add Stock", callback_data="admin_add_stock") # NEW
    )
    return markup
