# https://docs.python.org/3/library/sqlite3.html

import os
import sqlite3


def connect_db(db_path='db/orders.db'):
    if not os.path.exists(db_path):
        return "File not found"
    return sqlite3.connect(db_path)


def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        if query.strip().lower().startswith("select"):
            columns = []
            for description in cursor.description:
                columns.append(description[0])
            return columns, rows
        else:
            cursor.execute(query)
            conn.commit()
            return True
    except Exception as e:
        return f"Error: {e}"
