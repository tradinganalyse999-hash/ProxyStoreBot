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
        "vpn": [
            ("Nord VPN 1 Month", 25.00), ("Hma Vpn 7 Days", 30.00), ("Proton Vpn 14 Day", 50.00),
            ("Surfshark 7 Days", 25.00), ("Hotspot Shield 7 Days", 25.00), ("Cyber Ghost Vpn 3 Day", 20.00),
            ("Avast 7 Days", 25.00), ("Vpn - Viper 3 Days", 25.00), ("Ip Vanish 7 Days", 25.00),
            ("Pia 7 Days", 25.00), ("Pure 7 Days", 25.00), ("Potato 7 Days", 25.00), 
            ("Sky 7 Days", 25.00), ("Turbo 7 Days", 25.00)
        ],
        "proxy": [("Owl Proxy 200MB", 10.00)],
        "gmail": [("Gmail", 50.00)],
        "outlook": [("Outlook.com", 0.80)],
        "hotmail": [("Hotmail.com", 0.80)],
        "Morelogin": [("Morelogin 100 Minutes", 0.80)]
    }
    for name, price in products.get(category, []):
        markup.add(InlineKeyboardButton(f"🛒 {name} - 💎 {price} BDT", callback_data=f"select_qty|{category}|{name}|{price}"))
    markup.add(InlineKeyboardButton("⬅️ Back", callback_data="shop"))
    return markup

def quantity_menu(category, name, price, qty):
    total = price * qty
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("➖", callback_data=f"qty_minus|{category}|{name}|{price}|{qty}"),
        InlineKeyboardButton(f"{qty}", callback_data="noop"),
        InlineKeyboardButton("➕", callback_data=f"qty_plus|{category}|{name}|{price}|{qty}")
    )
    markup.add(InlineKeyboardButton("📝 Custom Quantity", callback_data=f"custom_qty|{category}|{name}|{price}"))
    markup.add(
        InlineKeyboardButton(f"✅ কনফার্ম {total:.2f} BDT", callback_data=f"buy|{category}|{name}|{price}|{qty}"),
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
