import sqlite3

def connect_database():
    #Creates a new database connection if it doesn't exist
    conn = sqlite3.connect('planner.db')
    return conn



print('database.py Running')
connect_database()