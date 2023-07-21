import os
import sqlite3

dir_extension = os.path.dirname(os.path.abspath(__file__))

def initialize_database():
    
    conn = sqlite3.connect(os.path.join(dir_extension, "sqlite.db"))
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            path TEXT,
            width INTEGER,
            height INTEGER
        )
    ''')

    conn.commit()
    conn.close()

initialize_database()