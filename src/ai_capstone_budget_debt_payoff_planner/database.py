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
                min_payment REAL NOT NULL,
                is_active INTEGER DEFAULT 1
            );
        """)
        #   Save data 
        conn.commit()
        print('init_db running. Tables created')

def delete_all_tables():
    """Deletes all tables (income, expenses, debts) from database"""
    with connect_database() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM income")
        cursor.execute("DELETE FROM expenses")
        cursor.execute("DELETE FROM debts")
        conn.commit()


# *************************************
# *****   INCOME CRUD FUNCTIONS   *****
# *************************************
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

def show_all_income():
    """Retrieves all income sources"""
    with connect_database() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM income"
            )
        conn.commit()
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def delete_income(income_id):
    """Deletes an income record by ID."""
    with connect_database() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
        conn.commit()

# ***************************************
# *****   EXPENSES CRUD FUNCTIONS   *****
# ***************************************
def add_expense(description, amount, category):
    """Stores an expense record """
    with connect_database() as conn:
        cursor = conn.cursor()
        #   Using parameterized queries to prevent SQL injection attacks
        cursor.execute(
            "INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?);", (description, amount, category)
        )
        conn.commit()
        return cursor.lastrowid

def show_all_expenses():
    """Retrieves all expenses records"""
    with connect_database() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM expenses"
            )
        conn.commit()
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def delete_expense(expense_id):
    """Deletes an expense record by ID."""
    with connect_database() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()


# ***************************************
# *****   DEBTS CRUD FUNCTIONS   *****
# ***************************************
def add_debt(name, balance, apr, min_payment):
    "Stores debt into debts table"
    with connect_database() as conn:
        cursor = conn.cursor()
        #   Using parameterized queries to prevent SQL injection attacks
        cursor.execute(
            "INSERT INTO debts (name, balance, apr, min_payment, is_active) VALUES (?, ?, ?, ?, ?);", (name, balance, apr, min_payment, 1)
        )
        conn.commit()
        return cursor.lastrowid

def show_all_debts():
    """Retrieves all debts records"""
    with connect_database() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM debts"
            )
        conn.commit()
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def delete_debt(debt_id):
    """Deletes a debt record by ID."""
    with connect_database() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM debts WHERE id = ?", (debt_id,))
        conn.commit()

def active(debt_id):
    """Changes is_active status to FALSE when debt is paid off"""
    with connect_database() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE debts SET is_active = FALSE WHERE id = ?", (debt_id))