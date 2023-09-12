import os
import sqlite3

dir_extension = os.path.dirname(os.path.abspath(__file__))

def initialize_database():
    with sqlite3.connect(os.path.join(dir_extension, "sqlite.db")) as conn:
        print("Install sd-masonry...")
        c = conn.cursor()

        # Create the 'version' table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS version (
                id INTEGER PRIMARY KEY,
                schema_version INTEGER
            )
        ''')

        # Check the current schema version
        c.execute('''SELECT schema_version FROM version LIMIT 1''')
        result = c.fetchone()

        # If the 'version' table is empty, set the initial schema version
        if result is None:
            current_version = 0
            c.execute('INSERT INTO version (schema_version) VALUES (?)', (0,))
        else:
            current_version = result[0]
        
        print("Found version v{}".format(current_version))
        
        # Setup our images db
        if current_version == 0:
            # Drop the table for those who already downloaded
            c.execute('''
                DROP TABLE IF EXISTS images 
            ''')

            # Create with new columns
            c.execute('''
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY,
                    path TEXT,
                    width INTEGER,
                    height INTEGER,
                    geninfo TEXT
                )
            ''')
            current_version = current_version + 1
            conn.commit()

        # Update the 'version' table with the new version number
        c.execute('UPDATE version SET schema_version = ?', (current_version,))

initialize_database()