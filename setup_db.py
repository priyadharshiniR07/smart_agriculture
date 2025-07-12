import sqlite3

# Connect (creates database.db if it doesn't exist)
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        soil_moisture REAL,
        temperature REAL,
        humidity REAL,
        rainfall INTEGER
    )
''')

conn.commit()
conn.close()

print("Database and table created successfully.")
