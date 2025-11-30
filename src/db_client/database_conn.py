import os
import sqlite3
from sqlite3 import Connection
from ..config.logger import logger

# from __future__ import annotations

# ------------------------------------------------------------------------------
# Database Connection
# ------------------------------------------------------------------------------

ABSOLUTE_PATH: str | None = os.getenv("DATABASE_ABSOLUTE_PATH", None)
ROOT_PATH = os.getcwd()
RELATIVE_PATH = "database/data/sample.db"
DB_PATH = ABSOLUTE_PATH if ABSOLUTE_PATH else os.path.join(ROOT_PATH, RELATIVE_PATH)


# SINGLETON
class DatabaseConnection:
    # _instance: DatabaseConnection | None = None  # Singleton instance
    _instance = None  # Singleton instance

    def __new__(cls, path: str = DB_PATH):
        # Si ya existe una instancia, se reutiliza
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialize(path)

        return cls._instance

    def __initialize(self, path: str = DB_PATH):
        self.__connection: Connection | None = None
        self.__tables_and_columns: dict | None = None
        self.db_path: str = path

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

    def get_tables_and_columns(self, exclude_tables: list[str] = []) -> dict:
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
            if table_name in exclude_tables:
                continue

            cur.execute(f"PRAGMA table_info('{table_name}');")
            cols_rows = cur.fetchall()

            columns = []
            for _, name, col_type, _, _, _ in cols_rows:
                columns.append({"name": name, "type": col_type})

            data["tables"][table_name] = {"columns": columns}

        self.__tables_and_columns = data
        return self.__tables_and_columns

    def get_table(self, table_name: str) -> dict:
        conn = self.connection
        cur = conn.cursor()

        cur.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%';
            """
        )

        tablas = [row[0] for row in cur.fetchall()]

        for _table_name in tablas:
            if _table_name == table_name:
                cur.execute(f"PRAGMA table_info('{table_name}');")
                cols_rows = cur.fetchall()
                columns = []
                for _, name, col_type, _, _, _ in cols_rows:
                    columns.append({"name": name, "type": col_type})
                return {table_name: {"columns": columns}}

        return {}
