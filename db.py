import sqlite3

DB_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_table():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            weekday TEXT,
            month TEXT,
            week_in_month INTEGER,
            amount REAL,
            type TEXT,
            comments TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def insert_expense(date, weekday, month, week_in_month, amount, exp_type, comments):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO expenses (date, weekday, month, week_in_month, amount, type, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (date, weekday, month, week_in_month, amount, exp_type, comments),
    )
    conn.commit()
    conn.close()


def fetch_all():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
