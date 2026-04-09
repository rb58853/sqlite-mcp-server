import os
import sqlite3
import argparse
from pathlib import Path


def resolve_db_path() -> Path:
    """Resolve database file path independently from the current working directory."""
    env_path = os.getenv("DATABASE_ABSOLUTE_PATH")
    project_root = Path(__file__).resolve().parents[1]

    if env_path:
        expanded = Path(env_path).expanduser()
        return expanded if expanded.is_absolute() else project_root / expanded

    return project_root / "database" / "data" / "sample.db"


def create_seed_data() -> tuple[list[tuple], list[tuple], list[tuple]]:
    sales = [
        ("iPhone 14", "smartphones", 1300, "Argentina", "2024-05-10"),
        ("MacBook Air M3", "notebooks", 1800, "Chile", "2024-05-12"),
        ("Samsung Galaxy S24", "smartphones", 1150, "Colombia", "2024-05-14"),
        ("Dell XPS 13", "notebooks", 1650, "Peru", "2024-05-16"),
        ("Lenovo ThinkPad X1", "notebooks", 1950, "Mexico", "2024-05-20"),
        ("iPad Pro", "tablets", 1400, "Argentina", "2024-05-22"),
        ("Surface Pro 9", "tablets", 1500, "Chile", "2024-05-25"),
        ("AirPods Pro", "accessories", 320, "Uruguay", "2024-05-28"),
        ("Sony WH-1000XM5", "accessories", 410, "Argentina", "2024-06-01"),
        ("Apple Watch Series 9", "wearables", 520, "Brazil", "2024-06-03"),
        ("Garmin Fenix 7", "wearables", 680, "Colombia", "2024-06-05"),
        ("GoPro Hero 12", "cameras", 760, "Mexico", "2024-06-08"),
        ("Canon EOS R50", "cameras", 980, "Peru", "2024-06-10"),
        ("Logitech MX Master 3S", "accessories", 140, "Chile", "2024-06-13"),
        ("Mechanical Keyboard K8", "accessories", 120, "Argentina", "2024-06-15"),
        ("ASUS ROG Zephyrus", "notebooks", 2300, "United States", "2024-06-18"),
        ("Acer Swift Go", "notebooks", 1250, "Ecuador", "2024-06-20"),
        ("Google Pixel 8", "smartphones", 980, "Costa Rica", "2024-06-22"),
        ("Xiaomi 14", "smartphones", 840, "Mexico", "2024-06-24"),
        ("OnePlus 12", "smartphones", 910, "Colombia", "2024-06-26"),
        ("DJI Mini 4 Pro", "drones", 1200, "Chile", "2024-07-01"),
        ("Meta Quest 3", "vr", 780, "Argentina", "2024-07-04"),
        ("Nintendo Switch OLED", "gaming", 470, "Peru", "2024-07-06"),
        ("PlayStation 5", "gaming", 690, "Mexico", "2024-07-09"),
        ("Xbox Series X", "gaming", 640, "Brazil", "2024-07-11"),
        ("Samsung Odyssey G7", "monitors", 890, "Uruguay", "2024-07-14"),
        ("LG UltraFine 5K", "monitors", 1600, "Chile", "2024-07-16"),
        ("Kindle Scribe", "tablets", 430, "Argentina", "2024-07-18"),
        ("Raspberry Pi 5 Kit", "iot", 260, "Colombia", "2024-07-21"),
        ("NVIDIA Jetson Orin Nano", "iot", 560, "Mexico", "2024-07-23"),
        ("HP LaserJet Pro", "printers", 390, "Peru", "2024-07-25"),
        ("Epson EcoTank L3250", "printers", 350, "Argentina", "2024-07-27"),
        ("TP-Link Deco X50", "networking", 280, "Chile", "2024-07-30"),
        ("Ubiquiti UniFi 6", "networking", 330, "Colombia", "2024-08-01"),
        ("Synology DS224+", "storage", 610, "Mexico", "2024-08-03"),
        ("WD My Cloud EX2", "storage", 520, "Brazil", "2024-08-05"),
    ]

    clientes = [
        ("Pedro Alvarez", "+56 9 81234567", "pedro.alvarez@empresa.cl", "Gran Empresa", "Chile"),
        ("Maria Torres", "+54 9 11 2345 6789", "maria.torres@iberdata.com.ar", "Mediana Empresa", "Argentina"),
        ("Luis Romero", "+52 55 1234 9876", "luis.romero@soluciones.mx", "Pequena Empresa", "Mexico"),
        ("Camila Perez", "+1 305 789 1234", "camila.perez@latamcorp.com", "Gran Empresa", "United States"),
        ("Jorge Martinez", "+57 317 456 8920", "jorge.martinez@andes.com.co", "Mediana Empresa", "Colombia"),
        ("Ana Fernandez", "+54 9 11 2045 6789", "ana.fernandez@pampatech.com.ar", "Pequena Empresa", "Argentina"),
        ("Daniel Rodriguez", "+1 213 555 7890", "daniel.rodriguez@usacorp.com", "Gran Empresa", "United States"),
        ("Sara Lopez", "+39 347 123 4567", "sara.lopez@mediterranea.it", "Mediana Empresa", "Italy"),
        ("Carlos Herrera", "+56 9 82224567", "carlos.herrera@andesplus.cl", "Pequena Empresa", "Chile"),
        ("Lucia Gonzalez", "+44 7400 123456", "lucia.gonzalez@ukpartners.co.uk", "Gran Empresa", "United Kingdom"),
        ("Valentina Rios", "+57 300 987 6543", "valentina.rios@nova.com.co", "Mediana Empresa", "Colombia"),
        ("Sebastian Paredes", "+51 999 123 456", "sebastian.paredes@inca.pe", "Pequena Empresa", "Peru"),
        ("Gabriela Mendez", "+52 55 9876 4321", "gabriela.mendez@azteca.mx", "Gran Empresa", "Mexico"),
        ("Tomas Silva", "+55 11 99876 4321", "tomas.silva@paulista.com.br", "Mediana Empresa", "Brazil"),
        ("Isabella Costa", "+55 21 91234 5678", "isabella.costa@riohub.com.br", "Pequena Empresa", "Brazil"),
        ("Matias Fuentes", "+56 9 7333 9988", "matias.fuentes@andeslabs.cl", "Gran Empresa", "Chile"),
        ("Renata Duarte", "+351 912 345 678", "renata.duarte@porto.pt", "Mediana Empresa", "Portugal"),
        ("Nicolas Cabrera", "+598 94 123 456", "nicolas.cabrera@uytech.uy", "Pequena Empresa", "Uruguay"),
        ("Elena Rossi", "+39 348 555 2121", "elena.rossi@milano.it", "Gran Empresa", "Italy"),
        ("Martin Vega", "+54 9 351 123 4567", "martin.vega@cordoba.ar", "Mediana Empresa", "Argentina"),
    ]

    ordenes = [
        (1, 1, 2, "completed", "online", "2024-08-06"),
        (2, 3, 1, "completed", "reseller", "2024-08-07"),
        (3, 6, 3, "pending", "online", "2024-08-07"),
        (4, 10, 1, "completed", "retail", "2024-08-08"),
        (5, 2, 1, "cancelled", "online", "2024-08-08"),
        (6, 9, 4, "completed", "partner", "2024-08-09"),
        (7, 12, 1, "pending", "online", "2024-08-10"),
        (8, 15, 2, "completed", "retail", "2024-08-11"),
        (9, 7, 1, "completed", "reseller", "2024-08-11"),
        (10, 5, 5, "completed", "partner", "2024-08-12"),
        (11, 4, 1, "pending", "online", "2024-08-13"),
        (12, 11, 2, "completed", "retail", "2024-08-13"),
        (13, 16, 1, "completed", "online", "2024-08-14"),
        (14, 19, 2, "cancelled", "reseller", "2024-08-14"),
        (15, 20, 1, "completed", "partner", "2024-08-15"),
        (16, 21, 1, "completed", "online", "2024-08-15"),
        (17, 22, 3, "pending", "retail", "2024-08-16"),
        (18, 23, 2, "completed", "online", "2024-08-16"),
        (19, 24, 1, "completed", "reseller", "2024-08-17"),
        (20, 25, 2, "completed", "partner", "2024-08-17"),
        (1, 26, 1, "completed", "online", "2024-08-18"),
        (2, 27, 1, "pending", "retail", "2024-08-18"),
        (3, 28, 2, "completed", "online", "2024-08-19"),
        (4, 29, 1, "completed", "reseller", "2024-08-19"),
        (5, 30, 1, "pending", "partner", "2024-08-20"),
        (6, 31, 2, "completed", "online", "2024-08-20"),
        (7, 32, 1, "completed", "retail", "2024-08-21"),
        (8, 33, 3, "completed", "reseller", "2024-08-21"),
        (9, 34, 1, "cancelled", "online", "2024-08-22"),
        (10, 35, 2, "completed", "partner", "2024-08-22"),
        (11, 36, 1, "completed", "retail", "2024-08-23"),
        (12, 18, 2, "pending", "online", "2024-08-23"),
        (13, 14, 1, "completed", "reseller", "2024-08-24"),
        (14, 8, 2, "completed", "partner", "2024-08-24"),
        (15, 13, 1, "completed", "online", "2024-08-25"),
        (16, 17, 2, "completed", "retail", "2024-08-25"),
        (17, 6, 1, "pending", "online", "2024-08-26"),
        (18, 2, 2, "completed", "reseller", "2024-08-26"),
        (19, 1, 1, "completed", "partner", "2024-08-27"),
        (20, 10, 1, "completed", "online", "2024-08-27"),
    ]

    return sales, clientes, ordenes


def main(only_if_missing: bool = False) -> None:
    db_path = resolve_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if db_path.exists():
        if only_if_missing:
            print(f"Sample DB already exists at {db_path}. Skipping rebuild.")
            return
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ordenes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        venta_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        estado TEXT NOT NULL,
        canal TEXT NOT NULL,
        fecha_orden TEXT NOT NULL,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id),
        FOREIGN KEY(venta_id) REFERENCES ventas(id)
    )"""
    )

    sales, clientes, ordenes = create_seed_data()

    cursor.executemany(
        """
        INSERT INTO ventas (producto, categoria, precio, pais, fecha_venta)
        VALUES (?, ?, ?, ?, ?)
    """,
        sales,
    )

    cursor.executemany(
        """
        INSERT INTO clientes (nombre, telefono, correo, tipo_de_empresa, pais)
        VALUES (?, ?, ?, ?, ?)
    """,
        clientes,
    )

    cursor.executemany(
        """
        INSERT INTO ordenes (cliente_id, venta_id, cantidad, estado, canal, fecha_orden)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        ordenes,
    )

    conn.commit()
    conn.close()

    print(f"Sample DB rebuilt at {db_path}")
    print(
        f"Inserted {len(sales)} rows into ventas, "
        f"{len(clientes)} rows into clientes and {len(ordenes)} rows into ordenes."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create/rebuild sample SQLite DB")
    parser.add_argument(
        "--if-missing",
        action="store_true",
        help="Only create the DB if it does not exist yet.",
    )
    args = parser.parse_args()
    main(only_if_missing=args.if_missing)
