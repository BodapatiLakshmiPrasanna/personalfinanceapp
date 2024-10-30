# database.py
import sqlite3

DB_NAME = "finance_manager.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                      )''')
    
    # Create transactions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        type TEXT,
                        category TEXT,
                        amount REAL,
                        date TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                      )''')
    
    # Create budgets table, with "limit" in quotes to avoid SQL syntax error
    cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        category TEXT,
                        "limit" REAL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                      )''')
    
    conn.commit()
    conn.close()

    # Confirmation message
    print("Database and tables created successfully.")

# Run the function if the script is executed directly
if __name__ == "__main__":
    create_tables()
