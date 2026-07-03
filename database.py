import sqlite3

DB_NAME = "studyplanner.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS exams(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        exam_date TEXT
    )
    """)

    conn.commit()
    conn.close()