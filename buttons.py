from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🛒 Shop", callback_data="shop"),
               InlineKeyboardButton("👛 Wallet", callback_data="wallet"))
    markup.add(InlineKeyboardButton("📦 My Orders", callback_data="orders"),
               InlineKeyboardButton("💰 Deposit", callback_data="deposit"))
    markup.add(InlineKeyboardButton("👥 Refer", callback_data="refer"),
               InlineKeyboardButton("🆘 Support", callback_data="support"))
    markup.add(InlineKeyboardButton("ℹ️ About", callback_data="about"))
    return markup

def shop_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🌐 VPN", callback_data="vpn_list"))
    markup.add(InlineKeyboardButton("🌍 Proxy", callback_data="proxy_list"))
    markup.add(InlineKeyboardButton("📧 Gmail", callback_data="gmail_list"))
    markup.add(InlineKeyboardButton("📮 Outlook", callback_data="outlook_list"))
    markup.add(InlineKeyboardButton("📬 Hotmail", callback_data="hotmail_list"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def product_menu(category):
    markup = InlineKeyboardMarkup(row_width=1)
    products = {
        "vpn": [("Owl Proxy 200MB", 5.00), ("Nord VPN 1 Month", 150.00)],
        "proxy": [("Residential Proxy 1GB", 20.00)],
        "gmail": [("Gmail Old 2018", 10.00)],
        "outlook": [("Outlook Fresh", 8.00)],
        "hotmail": [("Hotmail Aged", 7.00)]
    }
    for name, price in products.get(category, []):
        markup.add(InlineKeyboardButton(f"🛒 {name} - 💎 {price} BDT", callback_data=f"qty_{category}_{name}_{price}"))
    markup.add(InlineKeyboardButton("⬅️ Back", callback_data="shop"))
    return markup

def quantity_menu(category, name, price, qty):
    total = price * qty
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("➖", callback_data=f"dec_{category}_{name}_{price}_{qty}"),
        InlineKeyboardButton(f"{qty}", callback_data="none"),
        InlineKeyboardButton("➕", callback_data=f"inc_{category}_{name}_{price}_{qty}")
    )
    markup.add(InlineKeyboardButton("📝 Custom Quantity", callback_data=f"custom_{category}_{name}_{price}"))
    markup.add(
        InlineKeyboardButton(f"✅ কনফার্ম {total} BDT", callback_data=f"confirm_{category}_{name}_{price}_{qty}"),
        InlineKeyboardButton("❌ Cancel", callback_data=f"{category}_list")
    )
    return markup

def deposit_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("bKash", callback_data="bkash"),
               InlineKeyboardButton("Nagad", callback_data="nagad"))
    markup.add(InlineKeyboardButton("Rocket", callback_data="rocket"),
               InlineKeyboardButton("USDT", callback_data="usdt"))
    markup.add(InlineKeyboardButton("📤 Payment Submit", callback_data="submit_payment"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup
