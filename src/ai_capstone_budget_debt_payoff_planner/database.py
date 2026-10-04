import sqlite3

def connect_database():
    """Creates a new database connection if it doesn't exist"""
    conn = sqlite3.connect('planner.db')
    return conn

def init_db():
    """Initializes SQLite schema tables for income, expenses and debts"""
    #"with" simplifies resource management by automatically handling setup and cleanup of conn even if error or exception
    with connect_database() as conn:
        #Creates a db cursor to execute SQL statements and fetch results from SQL queries
        cur = conn.cursor()
        print('init_db running')







# print('database.py Running')
# connect_database()
init_db()