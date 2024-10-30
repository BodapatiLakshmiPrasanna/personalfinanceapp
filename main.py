# main.py
import getpass
from database import create_tables  # This imports the database setup function
from user_functions import register, login, add_transaction, update_transaction, delete_transaction, generate_report, set_budget

# Run create_tables to ensure database and tables are set up
create_tables()

def main():
    print("Welcome to the Personal Finance Management App!")
    while True:
        action = input("Choose an action: [register, login, quit]: ").strip().lower()
        if action == 'register':
            username = input("Enter a username: ")
            password = getpass.getpass("Enter a password: ")
            register(username, password)
        elif action == 'login':
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            user = login(username, password)
            if user:
                print("Login successful.")
                user_session(user)
            else:
                print("Login failed. Please try again.")
        elif action == 'quit':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def user_session(user):
    while True:
        action = input("Choose action: [add, update, delete, report, budget, logout]: ").strip().lower()
        if action == 'add':
            trans_type = input("Type [Income/Expense]: ").capitalize()
            category = input("Category: ")
            amount = float(input("Amount: "))
            add_transaction(user['id'], trans_type, category, amount)
        elif action == 'update':
            trans_id = int(input("Transaction ID to update: "))
            category = input("New category (leave blank to skip): ").strip()
            amount = input("New amount (leave blank to skip): ").strip()
            amount = float(amount) if amount else None
            update_transaction(trans_id, category, amount)
        elif action == 'delete':
            trans_id = int(input("Transaction ID to delete: "))
            delete_transaction(trans_id)
        elif action == 'report':
            generate_report(user['id'])
        elif action == 'budget':
            category = input("Category: ")
            limit = float(input("Budget limit: "))
            set_budget(user['id'], category, limit)
        elif action == 'logout':
            print("Logged out.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
