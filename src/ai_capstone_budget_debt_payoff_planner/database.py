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


# ***************************************
# *****   DEBTS CRUD FUNCTIONS   *****
# ***************************************
def add_debt(name, balance, apr, min_payment):
    "Stores debt into debts table"
    with connect_database() as conn:
        cursor = conn.cursor()
        #   Using parameterized queries to prevent SQL injection attacks
        cursor.execute(
            "INSERT INTO debts (name, balance, apr, min_payment) VALUES (?, ?, ?, ?);", (name, balance, apr, min_payment)
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



# print('database.py Running')
# connect_database()
# init_db()

# lastRowID = add_income('work', 100)
# print('lastRowID ', lastRowID)
# print(show_all_income())
# add_income('work2', 120)
# add_income('work3', 'd')
# print(show_all_income())

# expense_lastRowID = add_expense('Target', 35, 'Groceries')
# print('Expenses: ', expense_lastRowID)
# expense_lastRowID = add_expense('CVS', 50, 'Clothing')
# print('Expenses: ', expense_lastRowID)
# print(show_all_expenses())

debt_lastRowID = add_debt('Personal loan', 200, 8, 5)
print('Debt: ', debt_lastRowID)
debt_lastRowID = add_debt('Credit card', 50, 19.88, 12)
print('Debt: ', debt_lastRowID)
print(show_all_debts())
