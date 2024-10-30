# user_functions.py
import sqlite3
from hashlib import sha256

DB_NAME = "finance_manager.db"

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def register(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("Registration successful.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()

def login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {'id': user[0], 'username': user[1]}
    return None

def add_transaction(user_id, trans_type, category, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, ?, ?, ?, date('now'))",
                   (user_id, trans_type, category, amount))
    conn.commit()
    conn.close()
    print(f"{trans_type} recorded.")

def update_transaction(trans_id, category=None, amount=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if category:
        cursor.execute("UPDATE transactions SET category = ? WHERE id = ?", (category, trans_id))
    if amount:
        cursor.execute("UPDATE transactions SET amount = ? WHERE id = ?", (amount, trans_id))
    conn.commit()
    conn.close()
    print("Transaction updated.")

def delete_transaction(trans_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
    conn.commit()
    conn.close()
    print("Transaction deleted.")

def generate_report(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT type, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY type", (user_id,))
    totals = cursor.fetchall()
    total_income = sum(amount for trans_type, amount in totals if trans_type == 'Income')
    total_expense = sum(amount for trans_type, amount in totals if trans_type == 'Expense')
    savings = total_income - total_expense
    conn.close()
    print(f"Total Income: {total_income}, Total Expense: {total_expense}, Savings: {savings}")

def set_budget(user_id, category, limit):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO budgets (user_id, category, \"limit\") VALUES (?, ?, ?)",
                   (user_id, category, limit))
    conn.commit()
    conn.close()
    print(f"Budget set for {category} at {limit}.")
