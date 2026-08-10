from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_JOIN_LINK
from database import c, USE_POSTGRES

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
        InlineKeyboardButton("📦 My Orders", callback_data="my_orders"),
        InlineKeyboardButton("👥 Refer & Earn", callback_data="refer")
    )
    markup.add(
        InlineKeyboardButton("💳 Deposit", callback_data="deposit"),
        InlineKeyboardButton("🆘 Support", callback_data="support")
    )
    return markup

def shop_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🌍 Proxy (Owl)", callback_data="cat_proxy"), InlineKeyboardButton("🖥 Morelogin", callback_data="cat_morelogin"))
    markup.add(InlineKeyboardButton("🌐 VPN", callback_data="cat_vpn"), InlineKeyboardButton("📧 Gmail", callback_data="cat_gmail"))
    markup.add(InlineKeyboardButton("📮 Outlook", callback_data="cat_outlook"), InlineKeyboardButton("📬 Hotmail", callback_data="cat_hotmail"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def deposit_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("📱 bKash", callback_data="bkash"), InlineKeyboardButton("📱 Nagad", callback_data="nagad"))
    markup.add(InlineKeyboardButton("🚀 Rocket", callback_data="rocket"), InlineKeyboardButton("💵 USDT", callback_data="usdt"))
    markup.add(InlineKeyboardButton("📤 Submit TRX ID", callback_data="submit_payment"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def product_menu(category):
    if USE_POSTGRES:
        c.execute("SELECT DISTINCT product_name FROM stock WHERE category=%s AND status='available'", (category,))
    else:
        c.execute("SELECT DISTINCT product_name FROM stock WHERE category=? AND status='available'", (category,))
    products = c.fetchall()
    markup = InlineKeyboardMarkup()
    if not products:
        markup.add(InlineKeyboardButton("❌ Stock Empty", callback_data="shop"))
    else:
        for p in products:
            name = p[0]
            markup.add(InlineKeyboardButton(f"📦 {name}", callback_data=f"product_{category}_{name}"))
    markup.add(InlineKeyboardButton("⬅ Back", callback_data="shop"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def quantity_menu(category, product_name, qty):
    from config import PRICE_200MB
    price_per = 60
    if "200MB" in product_name: price_per = 60
    elif "1GB" in product_name: price_per = 150
    elif "10GB" in product_name: price_per = 500
    elif "Morelogin" in product_name: price_per = 120
    else: price_per = 60

    total = price_per * qty
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("➖", callback_data=f"qty_minus_{category}_{product_name}_{qty}"),
        InlineKeyboardButton(f"{qty} pcs", callback_data="noop"),
        InlineKeyboardButton("➕", callback_data=f"qty_plus_{category}_{product_name}_{qty}")
    )
    markup.add(InlineKeyboardButton("✏️ Custom Quantity", callback_data=f"custom_qty_{category}_{product_name}"))
    markup.add(InlineKeyboardButton(f"🛒 Buy - {total} BDT", callback_data=f"buy_{category}_{product_name}_{qty}_{total}"))
    markup.add(InlineKeyboardButton("⬅ Back", callback_data=f"cat_{category}"))
    markup.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return markup

def confirm_deposit_menu(user_id, amount, trx_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{user_id}_{amount}_{trx_id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}_{amount}")
    )
    return markup
