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
    markup.add(InlineKeyboardButton("🛒 Shop", callback_data="shop"), InlineKeyboardButton("👛 Wallet", callback_data="wallet"))
    markup.add(InlineKeyboardButton("📦 My Orders", callback_data="orders"), InlineKeyboardButton("👥 Refer & Earn", callback_data="refer"))
    markup.add(InlineKeyboardButton("💳 Deposit", callback_data="deposit"), InlineKeyboardButton("🆘 Support", callback_data="support"))
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
    markup = InlineKeyboardMarkup()

    if category == "proxy":
        markup.add(InlineKeyboardButton("Owl Proxy 200MB 3 BDT", callback_data="select_qty|proxy|Owl Proxy 200MB|3"))
        markup.add(InlineKeyboardButton("ABC Proxy 1 GB 290 BDT", callback_data="select_qty|proxy|ABC Proxy 1 GB|290"))
        markup.add(InlineKeyboardButton("Dataimpluse Proxy 1 GB 150 BDT", callback_data="select_qty|proxy|Dataimpluse Proxy 1 GB|150"))
        markup.add(InlineKeyboardButton("Rapid Proxy 500 MB 80 BDT", callback_data="select_qty|proxy|Rapid Proxy 500 MB|80"))
    elif category == "morelogin":
        markup.add(InlineKeyboardButton("Morelogin 100 Minutes 30 BDT", callback_data="select_qty|morelogin|Morelogin 100 Minutes|30"))
    elif category == "vpn":
        markup.add(InlineKeyboardButton("Nord VPN 7 Days 25 BDT", callback_data="select_qty|vpn|Nord VPN 7 Days|25"))
        markup.add(InlineKeyboardButton("HMA VPN 7 Days 25 BDT", callback_data="select_qty|vpn|HMA VPN 7 Days|25"))
        markup.add(InlineKeyboardButton("Proton VPN 14 Days 50 BDT", callback_data="select_qty|vpn|Proton VPN 14 Days|50"))
        markup.add(InlineKeyboardButton("Surfshark 7 Days 25 BDT", callback_data="select_qty|vpn|Surfshark 7 Days|25"))
        markup.add(InlineKeyboardButton("Hotspot Shield 7 Days 25 BDT", callback_data="select_qty|vpn|Hotspot Shield 7 Days|25"))
        markup.add(InlineKeyboardButton("Cyber Ghost 7 Days 25 BDT", callback_data="select_qty|vpn|Cyber Ghost 7 Days|25"))
        markup.add(InlineKeyboardButton("Avast 7 Days 25 BDT", callback_data="select_qty|vpn|Avast 7 Days|25"))
        markup.add(InlineKeyboardButton("IP Vanish 7 Days 25 BDT", callback_data="select_qty|vpn|IP Vanish 7 Days|25"))
        markup.add(InlineKeyboardButton("PIA 7 Days 25 BDT", callback_data="select_qty|vpn|PIA 7 Days|25"))
        markup.add(InlineKeyboardButton("Pure 7 Days 25 BDT", callback_data="select_qty|vpn|Pure 7 Days|25"))
        markup.add(InlineKeyboardButton("Potato 7 Days 25 BDT", callback_data="select_qty|vpn|Potato 7 Days|25"))
        markup.add(InlineKeyboardButton("Sky 7 Days 25 BDT", callback_data="select_qty|vpn|Sky 7 Days|25"))
        markup.add(InlineKeyboardButton("Turbo 7 Days 25 BDT", callback_data="select_qty|vpn|Turbo 7 Days|25"))
    elif category == "gmail":
        markup.add(InlineKeyboardButton("Gmail.com 40 BDT", callback_data="select_qty|gmail|Gmail.com 40|40"))
    elif category == "outlook":
        markup.add(InlineKeyboardButton("Outlook Fresh 0.80 BDT", callback_data="select_qty|outlook|Outlook Fresh|0.80"))
    elif category == "hotmail":
        markup.add(InlineKeyboardButton("Hotmail Fresh 0.80 BDT", callback_data="select_qty|hotmail|Hotmail Fresh|0.80"))

    markup.add(InlineKeyboardButton("⬅ Back", callback_data="shop"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def quantity_menu(category, name, price, qty):
    total = float(price) * int(qty)
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton("➖", callback_data=f"qty_minus|{category}|{name}|{price}|{qty}"), InlineKeyboardButton(f"{qty} pcs", callback_data="noop"), InlineKeyboardButton("➕", callback_data=f"qty_plus|{category}|{name}|{price}|{qty}"))
    markup.add(InlineKeyboardButton("✏ Custom Quantity", callback_data=f"custom_qty|{category}|{name}|{price}"))
    markup.add(InlineKeyboardButton(f"🛒 Buy - {total} BDT", callback_data=f"buy|{category}|{name}|{price}|{qty}"))
    markup.add(InlineKeyboardButton("⬅ Back", callback_data=f"{category}_list"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup
