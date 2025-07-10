import sqlite3

def load_checkpoint():
    conn = sqlite3.connect('checkpoint.db')
    c = conn.cursor()
    c.execute('SELECT zip_index FROM checkpoint WHERE id=1')
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0