from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==== EKHAN THEKE PRICE CHANGE KORBA DAILY ====
PRICE_LIST = {
    "vpn": {
        "NordVPN 1 Week": 25,
        "ProtonVPN 14D": 50,
        "HMA VPN 7D": 25,
        "Surfshark 7D": 25
    },
    "proxy": {
        "OWL Proxy 200MB": 10,
        "ABC Proxy 1GB": 290,
        "Datamplas 1GB": 150
    },
    "gmail": {
        "Gmail 1pc": 30
    },
    "outlook": {
        "OUTLOOK 1PIS": 0.60
    },
    "hotmail": {
        "HOTMAIL 1 PIS": 0.60
    }
}
# ================================================

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🛒 Shop", callback_data="shop"),
        InlineKeyboardButton("💰 Deposit", callback_data="deposit")
    )
    markup.add(
        InlineKeyboardButton("👛 Wallet", callback_data="wallet"),
        InlineKeyboardButton("📦 Orders", callback_data="orders")
    )
    markup.add(
        InlineKeyboardButton("🆘 Support", callback_data="support"),
        InlineKeyboardButton("ℹ️ About", callback_data="about")
    )
    markup.add( # Eita add korlam
        InlineKeyboardButton("🚀 রেফার & আর্ন", callback_data="refer")
    )
    return markup

def shop_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🌐 VPN", callback_data="vpn_list"),
        InlineKeyboardButton("🌍 Proxy", callback_data="proxy_list")
    )
    markup.add(
        InlineKeyboardButton("📧 Gmail", callback_data="gmail_list"),
        InlineKeyboardButton("📮 Outlook", callback_data="outlook_list")
    )
    markup.add(
        InlineKeyboardButton("📬 Hotmail", callback_data="hotmail_list"),
        InlineKeyboardButton("🏠 Back", callback_data="home")
    )
    return markup

def product_menu(category):
    markup = InlineKeyboardMarkup(row_width=1)
    products = PRICE_LIST.get(category, {})
    for name, price in products.items():
        safe_name = name.replace(" ", "_")
        callback = f"buy_{category}_{safe_name}_{price}"
        markup.add(InlineKeyboardButton(f"{name} - {price} BDT", callback_data=callback))
    markup.add(InlineKeyboardButton("⬅️ Back", callback_data="shop"))
    return markup

def deposit_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💳 bKash", callback_data="bkash"),
        InlineKeyboardButton("💳 Nagad", callback_data="nagad")
    )
    markup.add(
        InlineKeyboardButton("🚀 Rocket", callback_data="rocket"),
        InlineKeyboardButton("💲 USDT", callback_data="usdt")
    )
    markup.add(InlineKeyboardButton("✅ Submit Payment", callback_data="submit_payment"))
    markup.add(InlineKeyboardButton("🏠 Back", callback_data="home"))
    return markup
