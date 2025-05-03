import sqlite3

conn = sqlite3.connect('tracker.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    company TEXT,
    role TEXT,
    status TEXT,
    job_desc TEXT,
    applied_on DATE
)
''')
conn.commit()
conn.close()