import sqlite3
from datetime import datetime

def save_checkpoint(zip_index):
    conn = sqlite3.connect('checkpoint.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO checkpoint (id, zip_index, updated_at)
        VALUES (1, ?, ?)
    ''', (zip_index, datetime.now().isoformat()))
    conn.commit()
    conn.close()