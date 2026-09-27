import sqlite3


def create_database():

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        gender TEXT,
        name TEXT,
        age TEXT,
        city TEXT,
        marital_status TEXT,
        education TEXT,
        job TEXT,
        height TEXT,
        clothing TEXT,
        religion TEXT,
        sect TEXT,
        about TEXT
    )
    """)

    connection.commit()
    connection.close()