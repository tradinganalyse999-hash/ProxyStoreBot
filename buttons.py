from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_JOIN_LINK

def force_join_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Channel Join Koro", url=FORCE_JOIN_LINK))
    markup.add(InlineKeyboardButton("✅ Verify", callback_data="verify_join"))
    return markup

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🛒 Shop", callback_data="shop"),
        InlineKeyboardButton("👛 Wallet", callback_data="wallet")
    )
    markup.add(
        InlineKeyboardButton("📦 My Orders", callback_data="orders"),
        InlineKeyboardButton("👥 Refer & Earn", callback_data="refer")
    )
    markup.add(
        InlineKeyboardButton("🆘 Support", callback_data="support"),
        InlineKeyboardButton("ℹ About", callback_data="about")
    )
    return markup

def shop_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🌍 Proxy", callback_data="proxy_list"))
    markup.add(InlineKeyboardButton("🖥 Morelogin", callback_data="morelogin_list"))
    markup.add(InlineKeyboardButton("🌐 VPN", callback_data="vpn_list"))
    markup.add(InlineKeyboardButton("📧 Gmail", callback_data="gmail_list"))
    markup.add(InlineKeyboardButton("📮 Outlook", callback_data="outlook_list"))
    markup.add(InlineKeyboardButton("📬 Hotmail", callback_data="hotmail_list"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def deposit_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("bKash", callback_data="bkash"),
        InlineKeyboardButton("Nagad", callback_data="nagad")
    )
    markup.add(
        InlineKeyboardButton("Rocket", callback_data="rocket"),
        InlineKeyboardButton("USDT", callback_data="usdt")
    )
    markup.add(InlineKeyboardButton("📤 Submit Payment", callback_data="submit_payment"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def product_menu(category):
    from database import c, USE_POSTGRES
    if USE_POSTGRES:
        c.execute("SELECT DISTINCT product_name FROM stock WHERE category=%s AND status='available'", (category,))
    else:
        c.execute("SELECT DISTINCT product_name FROM stock WHERE category=? AND status='available'", (category,))
    products = c.fetchall()
    markup = InlineKeyboardMarkup()
    for p in products:
        name = p[0]
        # price hardcoded for now, you can manage from config
        price = 50
        if "200MB" in name: price = 60
        markup.add(InlineKeyboardButton(f"{name}", callback_data=f"select_qty|{category}|{name}|{price}"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def quantity_menu(category, name, price, qty):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("➖", callback_data=f"qty_minus|{category}|{name}|{price}|{qty}"),
        InlineKeyboardButton(f"{qty} pcs", callback_data="noop"),
        InlineKeyboardButton("➕", callback_data=f"qty_plus|{category}|{name}|{price}|{qty}")
    )
    markup.add(InlineKeyboardButton("✏️ Custom Quantity", callback_data=f"custom_qty|{category}|{name}|{price}"))
    markup.add(InlineKeyboardButton(f"🛒 Buy - {price*qty} BDT", callback_data=f"buy|{category}|{name}|{price}|{qty}"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup
