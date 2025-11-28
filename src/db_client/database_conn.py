import os
import sqlite3
from sqlite3 import Connection
from ..config.logger import logger

# ------------------------------------------------------------------------------
# Database Connection
# ------------------------------------------------------------------------------

ABSOLUTE_PATH: str | None = os.getenv("DATABASE_ABSOLUTE_PATH", None)
ROOT_PATH = os.getcwd()
RELATIVE_PATH = "database/sample.db"
DB_PATH = ABSOLUTE_PATH if ABSOLUTE_PATH else os.path.join(ROOT_PATH, RELATIVE_PATH)


# SINGLETON
class DatabaseConnection:
    _instance = None

    def __new__(cls, path: str = DB_PATH):
        # Si ya existe una instancia, se reutiliza
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialize(path)

        return cls._instance

    def __initialize(self, path: str = DB_PATH):
        self.__connection: Connection | None = None
        self.__tables_and_columns: dict | None = None
        self.db_path = path

    @property
    def connection(self) -> Connection:
        if not self.__connection:
            try:
                # Connect to the SQLite database; disable thread check since this server is asynchronous.
                self.__connection = sqlite3.connect(
                    self.db_path, check_same_thread=False
                )
                # Set row_factory to sqlite3.Row so that rows can be accessed like dictionaries.
                self.__connection.row_factory = sqlite3.Row
                logger.info(f"Connected to SQLite database at '{self.db_path}'.")

            except Exception as e:
                # Log any errors in connecting to the database and raise the exception.
                logger.exception(f"Failed to connect to database '{self.db_path}': {e}")
                raise

        return self.__connection

    def get_tables_and_columns(self) -> dict:
        # cache simple
        if self.__tables_and_columns is not None:
            return self.__tables_and_columns

        conn = self.connection
        cur = conn.cursor()

        # 1) Obtener todas las tablas de usuario
        # sqlite_master es la tabla de metadatos de SQLite. [web:11][web:14]
        cur.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%';
            """
        )

        tablas = [row[0] for row in cur.fetchall()]

        data: dict = {"tables": {}}

        for table_name in tablas:
            # # 2) Info “genérica” de la tabla (puedes personalizar este texto)
            # info_tabla = f"Tabla {table_name} en la base de datos {self.db_path}"

            # 3) Obtener columnas de la tabla con PRAGMA
            cur.execute(
                f"PRAGMA table_info('{table_name}');"
            )  # devuelve cid, name, type, notnull, dflt_value, pk. [web:11][web:15]
            cols_rows = cur.fetchall()

            columns = []
            for _, name, col_type, _, _, _ in cols_rows:
                columns.append({"name": name, "type": col_type})

            data["tables"][table_name] = {
                "columns": columns,
            }

        self.__tables_and_columns = data
        return self.__tables_and_columns
