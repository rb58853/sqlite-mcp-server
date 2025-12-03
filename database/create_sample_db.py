import os
import sqlite3

ROOT_PATH = os.getcwd()
RELATIVE_PATH = "database/data/sample.db"
FILE_DB_PATH = os.path.join(ROOT_PATH, RELATIVE_PATH)

if os.path.exists(FILE_DB_PATH):
    os.remove(FILE_DB_PATH)

os.makedirs(os.path.dirname(FILE_DB_PATH), exist_ok=True)

# Connect to a new (or existing) SQLite database.
conn = sqlite3.connect(FILE_DB_PATH)
cursor = conn.cursor()

# region Sales Table
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
# endregion

# region Clients.
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT,
    tipo_de_empresa TEXT,
    pais TEXT
)"""
)

clientes = [
    (
        "Pedro Alvarez",
        "+56 9 81234567",
        "pedro.alvarez@empresa.cl",
        "Gran Empresa",
        "Chile",
    ),
    (
        "Maria Torres",
        "+54 9 11 2345 6789",
        "maria.torres@iberdata.com.ar",
        "Mediana Empresa",
        "Argentina",
    ),
    (
        "Luis Romero",
        "+52 55 1234 9876",
        "luis.romero@soluciones.mx",
        "Pequeña Empresa",
        "México",
    ),
    (
        "Camila Pérez",
        "+1 305 789 1234",
        "camila.perez@latamcorp.com",
        "Gran Empresa",
        "Estados Unidos",
    ),
    (
        "Jorge Martínez",
        "+57 317 456 8920",
        "jorge.martinez@andes.com.co",
        "Mediana Empresa",
        "Colombia",
    ),
    (
        "Ana Fernández",
        "+54 9 11 2345 6789",
        "ana.fernandez@pampatech.com.ar",
        "Pequeña Empresa",
        "Argentina",
    ),
    (
        "Daniel Rodríguez",
        "+1 213 555 7890",
        "daniel.rodriguez@usacorp.com",
        "Gran Empresa",
        "Estados Unidos",
    ),
    (
        "Sara López",
        "+39 347 123 4567",
        "sara.lopez@mediterranea.it",
        "Mediana Empresa",
        "Italia",
    ),
    (
        "Carlos Herrera",
        "+56 9 81234567",
        "carlos.herrera@andesplus.cl",
        "Pequeña Empresa",
        "Chile",
    ),
    (
        "Lucia González",
        "+44 7400 123456",
        "lucia.gonzalez@ukpartners.co.uk",
        "Gran Empresa",
        "Reino Unido",
    ),
]


cursor.executemany(
    """
    INSERT INTO clientes (nombre, telefono, correo, tipo_de_empresa, pais)
    VALUES (?, ?, ?, ?, ?)
""",
    clientes,
)
# endregion

conn.commit()
conn.close()
