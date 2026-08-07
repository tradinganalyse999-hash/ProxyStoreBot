import sqlite3

conn = sqlite3.connect("proxystore.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id INTEGER PRIMARY KEY,
              balance REAL DEFAULT 0,
              referred_by INTEGER DEFAULT NULL,
              referral_count INTEGER DEFAULT 0,
              total_referral_earning REAL DEFAULT 0)''')

c.execute('''CREATE TABLE IF NOT EXISTS orders
             (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, product TEXT, price REAL, status TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS referrals
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              referrer_id INTEGER,
              referred_id INTEGER UNIQUE,
              status TEXT DEFAULT 'pending')''')

c.execute('''CREATE TABLE IF NOT EXISTS deposits
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              amount REAL,
              trx_id TEXT,
              status TEXT DEFAULT 'pending')''')
conn.commit()

def create_user(user_id, referred_by=None):
    c.execute("INSERT OR IGNORE INTO users (user_id, referred_by) VALUES (?,?)", (user_id, referred_by))
    conn.commit()

def get_balance(user_id):
    c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    r = c.fetchone()
    return r[0] if r else 0

def update_balance(user_id, amount):
    create_user(user_id)
    c.execute("UPDATE users SET balance = balance +? WHERE user_id=?", (amount, user_id))
    conn.commit()

def add_order(user_id, product, price):
    c.execute("INSERT INTO orders (user_id, product, price, status) VALUES (?,?,?,?)",
              (user_id, product, price, "Pending"))
    conn.commit()
    return c.lastrowid # <-- EI LINE TA ADD KORSI

def get_orders(user_id):
    c.execute("SELECT product, price, status FROM orders WHERE user_id=? ORDER BY id DESC", (user_id,))
    return c.fetchall()

def get_order_by_id(order_id):
    c.execute("SELECT id, user_id, product, price, status FROM orders WHERE id=?", (order_id,))
    return c.fetchone()

def update_order_status(order_id, status):
    c.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()

def add_referral(referrer_id, referred_id):
    c.execute("INSERT OR IGNORE INTO referrals (referrer_id, referred_id) VALUES (?,?)", (referrer_id, referred_id))
    conn.commit()

def activate_referral_bonus(referred_id):
    c.execute("SELECT referrer_id FROM referrals WHERE referred_id=? AND status='pending'", (referred_id,))
    res = c.fetchone()
    if res:
        referrer_id = res[0]
        update_balance(referrer_id, 0.50)
        c.execute("UPDATE users SET referral_count = referral_count + 1, total_referral_earning = total_referral_earning + 0.50 WHERE user_id =?", (referrer_id,))
        c.execute("UPDATE referrals SET status='active' WHERE referred_id=?", (referred_id,))
        conn.commit()
        return referrer_id
    return None

def get_refer_stats(user_id):
    c.execute("SELECT referral_count, total_referral_earning FROM users WHERE user_id =?", (user_id,))
    data = c.fetchone()
    return data if data else (0, 0.0)

def add_deposit_request(user_id, amount, trx_id):
    c.execute("INSERT INTO deposits (user_id, amount, trx_id) VALUES (?,?,?)", (user_id, amount, trx_id))
    conn.commit()
    return c.lastrowid

def approve_deposit(deposit_id):
    c.execute("SELECT user_id, amount FROM deposits WHERE id=? AND status='pending'", (deposit_id,))
    res = c.fetchone()
    if res:
        user_id, amount = res
        update_balance(user_id, amount)
        c.execute("UPDATE deposits SET status='approved' WHERE id=?", (deposit_id,))
        conn.commit()
        return user_id, amount
    return None, None
