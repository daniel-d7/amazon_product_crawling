import sqlite3


def init_checkpoint_db():
    conn = sqlite3.connect('checkpoint.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS checkpoint (
            id INTEGER PRIMARY KEY,
            zip_index INTEGER,
            updated_at TEXT
        )
    ''')
    conn.commit()
    conn.close()