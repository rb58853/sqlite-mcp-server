import os
import sqlite3

ROOT_PATH = os.getcwd()
RELATIVE_PATH = "database/data/sample.db"
FILE_DB_PATH = os.path.join(ROOT_PATH, RELATIVE_PATH)

os.makedirs(os.path.dirname(FILE_DB_PATH), exist_ok=True)
        
# Connect to a new (or existing) SQLite database.
conn = sqlite3.connect(FILE_DB_PATH)
cursor = conn.cursor()

# Create a table for startup funding information.
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio INTEGER,
    pais TEXT,
    fecha_venta TEXT
)"""
)

# Insert some example records.
sales = [
    ("iPhone 14", "smartphones", 1300, "Argentina", "2024-05-10"),
    ("MacBook", "Airnotebooks", 1800, "Chile", "2024-05-12"),
]

cursor.executemany(
    """
    INSERT INTO ventas (producto, categoria, precio, pais, fecha_venta)
    VALUES (?, ?, ?, ?, ?)
""",
    sales,
)

conn.commit()
conn.close()
