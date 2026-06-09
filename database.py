import sqlite3

DB_NAME = "research.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        authors TEXT,
        year INTEGER,
        doi TEXT UNIQUE,
        journal TEXT,
        keyword TEXT,
        source TEXT
    )
    """)

    conn.commit()
    conn.close()
