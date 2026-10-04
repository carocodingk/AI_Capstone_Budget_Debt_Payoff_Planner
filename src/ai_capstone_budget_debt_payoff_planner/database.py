import sqlite3

def connect_database():
    """Creates a new database connection if it doesn't exist"""
    conn = sqlite3.connect('planner.db')
    # Indicates SQLite to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite schema tables for income, expenses and debts"""
    #   "with" simplifies resource management by automatically handling setup and cleanup of conn even if error or exception
    with connect_database() as conn:
        #   Creates a db cursor to execute SQL statements and fetch results from SQL queries
        cursor = conn.cursor()

        #   Income table 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL
            );
        """)

        #   Expense table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                description TEXT NOT NULL, 
                amount REAL NOT NULL,
                category TEXT NOT NULL
            );
        """)

        #   Debts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS debts (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, 
                balance REAL NOT NULL, 
                apr REAL NOT NULL, 
                min_payment REAL NOT NULL
            );
        """)
        #   Save data 
        conn.commit()
        print('init_db running. Tables created')

# *****   INCOME CRUD FUNCTIONS   *****
def add_income(name, amount):
    """Stores an income record """
    with connect_database() as conn:
        cursor = conn.cursor()
        #   Using parameterized queries to prevent SQL injection attacks
        cursor.execute(
            "INSERT INTO income (name, amount) VALUES (?, ?);", (name, amount)
        )
        conn.commit()
        return cursor.lastrowid







# print('database.py Running')
# connect_database()
# init_db()

# lastRowID = add_income('work', 100)
# print('lastRowID ', lastRowID)
# print(show_all_income())
show_all_income()