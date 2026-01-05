import sqlite3
import pandas as pd
import json

DB_NAME = "expenses.db"


# ---------------------- Core DB ----------------------
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_table():
    """Create the expenses table if it doesn't exist"""
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


# ---------------------- Insert ----------------------
def insert_expense(date, weekday, month, week_in_month, amount, exp_type, comments):
    """Insert a single expense"""
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


def add_expense_bulk(type_of_file, file_path):
    """
    Bulk insert expenses from CSV or JSON file.

    CSV format: date,weekday,month,week_in_month,amount,type,comments
    JSON format: list of dicts with keys matching table columns
    """
    conn = get_connection()
    cursor = conn.cursor()

    if type_of_file.lower() == "csv":
        df = pd.read_csv(file_path)
    elif type_of_file.lower() == "json":
        with open(file_path, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    else:
        raise ValueError("type_of_file must be 'csv' or 'json'")

    # Ensure all required columns exist
    required_cols = ["date", "weekday", "month", "week_in_month", "amount", "type", "comments"]
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns in file: {missing_cols}")

    # Bulk insert
    cursor.executemany(
        """
        INSERT INTO expenses (date, weekday, month, week_in_month, amount, type, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        df[required_cols].values.tolist()
    )
    conn.commit()
    conn.close()


# ---------------------- Fetch ----------------------
def fetch_all():
    """Fetch all expenses, ordered by date descending"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------------------- Delete ----------------------
def delete_expense_by_id(expense_id):
    """Delete a single expense by its primary key ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


def delete_expense_by_field(field_name, value):
    """
    Delete expenses by arbitrary column and value
    Example: delete_expense_by_field("type", "Food")
    """
    allowed_fields = ["id", "date", "weekday", "month", "week_in_month", "amount", "type", "comments"]
    if field_name not in allowed_fields:
        raise ValueError(f"{field_name} is not a valid column")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM expenses WHERE {field_name} = ?", (value,))
    conn.commit()
    conn.close()

# ---------------------- Update ----------------------
def update_expense_by_id(expense_id, **kwargs):
    """
    Update an expense row by ID.
    Only non-None kwargs are applied.
    Example: update_expense_by_id(3, amount=500, comments="New comment")
    """
    allowed_fields = ["date", "weekday", "month", "week_in_month", "amount", "type", "comments"]

    # Only include non-None values
    fields_to_update = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}

    if not fields_to_update:
        return  # Nothing to update

    set_clause = ", ".join([f"{k} = ?" for k in fields_to_update])
    values = list(fields_to_update.values())
    values.append(expense_id)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE expenses SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()
