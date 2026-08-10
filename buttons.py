from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_JOIN_LINK
import os

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
        InlineKeyboardButton("💳 Deposit", callback_data="deposit"),
        InlineKeyboardButton("🆘 Support", callback_data="support")
    )
    return markup

def shop_menu():
    markup = InlineKeyboardMarkup(row_width=2)
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
    markup.add(InlineKeyboardButton("📱 bKash", callback_data="bkash"), InlineKeyboardButton("📱 Nagad", callback_data="nagad"))
    markup.add(InlineKeyboardButton("🚀 Rocket", callback_data="rocket"), InlineKeyboardButton("💵 USDT", callback_data="usdt"))
    markup.add(InlineKeyboardButton("📤 Submit Payment", callback_data="submit_payment"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def product_menu(category):
    from database import c, USE_POSTGRES, get_stock_count
    # Stock check
    try:
        if USE_POSTGRES:
            c.execute("SELECT DISTINCT product_name FROM stock WHERE category=%s AND status='available'", (category,))
        else:
            c.execute("SELECT DISTINCT product_name FROM stock WHERE category=? AND status='available'", (category,))
        products = c.fetchall()
    except:
        products = []

    markup = InlineKeyboardMarkup()

    # Jodi stock e na thake, default products dekhao (tomar ager system er moto)
    if not products:
        if category == "proxy":
            markup.add(InlineKeyboardButton("Owl Proxy 200MB", callback_data="select_qty|proxy|Owl Proxy 200MB|60"))
            markup.add(InlineKeyboardButton("Owl Proxy 1GB", callback_data="select_qty|proxy|Owl Proxy 1GB|150"))
        elif category == "morelogin":
            markup.add(InlineKeyboardButton("Morelogin 100 Minutes", callback_data="select_qty|morelogin|Morelogin 100 Minutes|120"))
        elif category == "vpn":
            markup.add(InlineKeyboardButton("VPN 1 Month", callback_data="select_qty|vpn|VPN 1 Month|100"))
        elif category == "gmail":
            markup.add(InlineKeyboardButton("Gmail Fresh", callback_data="select_qty|gmail|Gmail Fresh|30"))
        elif category == "outlook":
            markup.add(InlineKeyboardButton("Outlook Fresh", callback_data="select_qty|outlook|Outlook Fresh|30"))
        elif category == "hotmail":
            markup.add(InlineKeyboardButton("Hotmail Fresh", callback_data="select_qty|hotmail|Hotmail Fresh|30"))
    else:
        for p in products:
            name = p[0]
            # Price logic
            price = 60
            if "200MB" in name: price = 60
            elif "1GB" in name: price = 150
            elif "10GB" in name: price = 500
            elif "Morelogin" in name: price = 120
            markup.add(InlineKeyboardButton(f"📦 {name} ({get_stock_count(category, name)} pcs)", callback_data=f"select_qty|{category}|{name}|{price}"))

    markup.add(InlineKeyboardButton("⬅ Back", callback_data="shop"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def quantity_menu(category, name, price, qty):
    total = price * qty
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("➖", callback_data=f"qty_minus|{category}|{name}|{price}|{qty}"),
        InlineKeyboardButton(f"{qty} pcs", callback_data="noop"),
        InlineKeyboardButton("➕", callback_data=f"qty_plus|{category}|{name}|{price}|{qty}")
    )
    markup.add(InlineKeyboardButton("✏️ Custom Quantity", callback_data=f"custom_qty|{category}|{name}|{price}"))
    markup.add(InlineKeyboardButton(f"🛒 Buy - {total} BDT", callback_data=f"buy|{category}|{name}|{price}|{qty}"))
    markup.add(InlineKeyboardButton("⬅ Back", callback_data=f"{category}_list"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup
