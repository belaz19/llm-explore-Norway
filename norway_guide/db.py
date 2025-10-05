import sqlite3

# Connect to database
conn = sqlite3.connect("monitor.db", check_same_thread=False)
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS monitor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    query TEXT,
    prompt TEXT,
    answer TEXT,
    feedback TEXT,
    response_time REAL,
    input_tokens INTEGER,
    output_tokens INTEGER
)
''')
conn.commit()

# Export connection and cursor
def get_connection():
    return conn

def get_cursor():
    return c