import os
import sqlite3
from sqlite3 import Connection
from ..config.logger import logger
# from __future__ import annotations

ABSOLUTE_PATH: str | None = os.getenv("DATABASE_ABSOLUTE_PATH", None)
"""Environment variable for absolute database path, or None if not set."""

ROOT_PATH = os.getcwd()
"""Current working directory as root path for relative database location."""

RELATIVE_PATH = "database/data/sample.db"
"""Relative path to the SQLite database file."""

DB_PATH = ABSOLUTE_PATH if ABSOLUTE_PATH else os.path.join(ROOT_PATH, RELATIVE_PATH)
"""Final database path, prioritizing absolute env var over relative path."""


# SINGLETON PATTERN FOR DATABASE CONNECTION
class DatabaseConnection:
    """Singleton class managing a single SQLite database connection.

    Ensures only one instance exists, providing thread-safe access in async contexts.
    Lazy-initializes connection and caches table metadata.
    """

    _instance = None  # Singleton instance reference


    def __new__(cls, path: str = DB_PATH) -> 'DatabaseConnection':
        """Create or return the singleton instance.

        Args:
            path: Database file path (defaults to DB_PATH).

        Returns:
            The single DatabaseConnection instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialize(path)
        return cls._instance  # Reuse existing instance


    def __initialize(self, path: str = DB_PATH) -> None:
        """Private initializer for the singleton instance.

        Args:
            path: Database file path.
        """
        
        self.__connection: Connection | None = None
        self.__tables_and_columns: dict | None = None
        self.db_path: str = path


    @property
    def connection(self) -> Connection:
        """Lazy property: establishes SQLite connection if not exists.

        Configures row_factory for dict-like row access and disables thread checks
        for async server compatibility. Logs connection success or failure.

        Returns:
            Active sqlite3.Connection instance.

        Raises:
            Exception: If connection fails (e.g., file access error).
        """
        if not self.__connection:
            try:
                # Connect to SQLite; disable thread check for async usage
                self.__connection = sqlite3.connect(
                    self.db_path, check_same_thread=False
                )
                # Enable dict-like row access
                self.__connection.row_factory = sqlite3.Row
                logger.info(f"Connected to SQLite database at '{self.db_path}'.")
            except Exception as e:
                # Log and re-raise connection errors
                logger.exception(f"Failed to connect to database '{self.db_path}': {e}")
                raise
        return self.__connection


    def get_tables_and_columns(self, exclude_tables: list[str] = []) -> dict:
        """Retrieve and cache schema info for all user tables (excluding sqlite_ internals).

        Simple in-memory cache; skips excluded tables.

        Args:
            exclude_tables: List of table names to ignore.

        Returns:
            dict: {"tables": {table_name: {"columns": [{"name": str, "type": str}]}}}.
        """
        # Return cached result if available
        if self.__tables_and_columns is not None:
            return self.__tables_and_columns

        conn = self.connection
        cur = conn.cursor()

        # Query sqlite_master for user-created tables (exclude system tables)
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

            # Get column schema via PRAGMA
            cur.execute(f"PRAGMA table_info('{table_name}');")
            cols_rows = cur.fetchall()

            columns = []
            for _, name, col_type, _, _, _ in cols_rows:
                columns.append({"name": name, "type": col_type})

            data["tables"][table_name] = {"columns": columns}

        # Cache and return schema
        self.__tables_and_columns = data
        return self.__tables_and_columns


    def get_table(self, table_name: str) -> dict:
        """Get schema for a specific user table, or empty dict if not found.

        Validates table exists via sqlite_master before querying PRAGMA.

        Args:
            table_name: Name of the table to inspect.

        Returns:
            dict: {table_name: {"columns": [{"name": str, "type": str}]}} or {}.
        """
        conn = self.connection
        cur = conn.cursor()

        # Check if table exists (user tables only)
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

        return {}  # Table not found
