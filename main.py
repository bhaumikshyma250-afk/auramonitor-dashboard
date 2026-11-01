
# main.py

from database.db_handler import init_db

if __name__ == "__main__":
    print("Initializing Database...")
    init_db()
    print("Database tables created successfully!")