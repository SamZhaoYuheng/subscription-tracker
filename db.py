import sqlite3

def init_db():
    conn = sqlite3.connect("subscriptions.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS subs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        platform TEXT,
        renew_date TEXT,
        cycle TEXT,
        amount REAL,
        currency TEXT,
        link TEXT,
        note TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_sub(name, platform, renew_date, cycle, amount, currency, link, note):
    conn = sqlite3.connect("subscriptions.db")
    c = conn.cursor()
    c.execute("INSERT INTO subs(name,platform,renew_date,cycle,amount,currency,link,note) VALUES (?,?,?,?,?,?,?,?)",
              (name,platform,str(renew_date),cycle,amount,currency,link,note))
    conn.commit()
    conn.close()

def get_all_sub():
    conn = sqlite3.connect("subscriptions.db")
    c = conn.cursor()
    c.execute("SELECT * FROM subs")
    rows = c.fetchall()
    cols = [desc[0] for desc in c.description]
    res = [dict(zip(cols, r)) for r in rows]
    conn.close()
    return res

def delete_sub(sub_id):
    conn = sqlite3.connect("subscriptions.db")
    c = conn.cursor()
    c.execute("DELETE FROM subs WHERE id=?", (sub_id,))
    conn.commit()
    conn.close()
