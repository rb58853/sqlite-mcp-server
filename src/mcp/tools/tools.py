import yaml
import json
import re
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from ...config.logger import logger
from ...db_client.database_conn import DatabaseConnection
from ..utils import base_db_context, clients_table_context


class Tools:
    """Manages MCP tools for database querying with schema-aware descriptions.

    Loads tool descriptions from YAML files and registers SQL query tools
    with FastMCP, enforcing SELECT-only queries for safety.
    """

    def __init__(self):
        """Initialize Tools with database connection and load descriptions."""
        self.db = DatabaseConnection()
        """Singleton database connection instance."""
        # db_tables_and_columns: dict = db.get_tables_and_columns()
        self.descriptions: dict[str, str] = {}
        """Cached tool descriptions from YAML files."""
        self.__load_descriptions()  # Load descriptions on init

    def __load_descriptions(self) -> None:
        """Load tool descriptions from all YAML files in descriptions directory.

        Raises:
            FileNotFoundError: If descriptions directory does not exist.
        """
        # Path to descriptions directory relative to this module
        descriptions_dir = Path(__file__).parent / "descriptions"

        # Validate directory existence
        if not descriptions_dir.exists():
            raise FileNotFoundError(
                f"Tool descriptions directory not found: {descriptions_dir}"
            )

        # Load each YAML file and merge descriptions
        for yaml_file in descriptions_dir.glob("*.yaml"):
            try:
                with open(yaml_file) as f:
                    tool_descriptions = yaml.safe_load(f)
                    if tool_descriptions:
                        self.descriptions.update(tool_descriptions)
            except Exception as e:
                raise Exception(
                    f"Error loading tool descriptions from {yaml_file}: {e}"
                )  # Simple error reporting

    def __get_description(self, tool_name: str) -> str:
        """Get prefixed description for a tool name.

        Args:
            tool_name: Name of the tool to describe.

        Returns:
            Full description string with base context prefix.
        """
        return base_db_context + self.descriptions.get(tool_name, "")

    def registry(self, mcp: FastMCP) -> None:
        """Register SQL query tools with the FastMCP instance.

        Args:
            mcp: FastMCP server instance to register tools with.
        """

        @mcp.tool(description=self.__get_description(tool_name="sql_query"))
        def sql_query(query: str) -> str:
            """Execute arbitrary SELECT query against the database.

            Args:
                query: SQL SELECT query string.

            Returns:
                JSON-formatted list of query results or error message.
            """
            return base_sql_query(query=query, db=self.db)

        @mcp.tool(
            description=clients_table_context
            + self.descriptions.get("clients_sql_query", "")
        )
        def clients_sql_query(query: str) -> str:
            """Execute SELECT query scoped to clients table.

            Args:
                query: SQL SELECT query (implicitly clients table scoped).

            Returns:
                JSON-formatted list of query results or error message.
            """
            return base_sql_query(query=query, db=self.db)  # Shared implementation


def base_sql_query(query: str, db: DatabaseConnection) -> str:
    """Execute safe SQL SELECT query and return JSON results.

    Enforces SELECT-only queries. Converts rows to dicts for JSON serialization.

    Args:
        query: SQL query string (must start with SELECT).
        db: DatabaseConnection instance.

    Returns:
        JSON string of query results (indented) or error message.

    Raises:
        Logs exceptions but returns error string instead of raising.
    """
    logger.debug(f"Entering sql_query() with query: {query}")

    normalized = query.strip()

    if not normalized:
        msg = "Error: Empty query."
        logger.warning(msg)
        return msg

    # Safety: Only read-only queries are permitted.
    # Accepts SELECT and CTEs (WITH ... SELECT ...).
    # Blocks mutation/DDL/transaction and multi-statement inputs.
    forbidden_tokens = (
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "detach",
        "vacuum",
        "pragma",
        "reindex",
        "analyze",
        "begin",
        "commit",
        "rollback",
        "savepoint",
        "release",
    )

    lowered = normalized.lower()
    if not (lowered.startswith("select") or lowered.startswith("with")):
        msg = "Error: Only read-only SELECT queries are allowed."
        logger.warning(f"Query rejected: {query}. {msg}")
        return msg

    if re.search(r";\s*\S", normalized):
        msg = "Error: Multiple SQL statements are not allowed."
        logger.warning(f"Query rejected: {query}. {msg}")
        return msg

    for token in forbidden_tokens:
        if re.search(rf"\b{token}\b", lowered):
            msg = "Error: Query contains non read-only SQL keywords."
            logger.warning(f"Query rejected: {query}. {msg}")
            return msg

    if not sqlite3_complete_query(normalized):
        msg = "Error: Query is incomplete or malformed."
        logger.warning(f"Query rejected: {query}. {msg}")
        return msg

    try:
        # Execute query and fetch all rows
        cursor = db.connection.execute(query)
        rows = [dict(row) for row in cursor.fetchall()]
        result = json.dumps(rows, indent=2)
        logger.debug(f"SQL query executed successfully. Result: {result}")
    except Exception as e:
        result = f"Error executing query: {e}"
        logger.exception(result)

    logger.debug("Exiting sql_query()")
    return result


def sqlite3_complete_query(query: str) -> bool:
    """Basic statement completeness check for SQLite-compatible input."""
    trimmed = query.strip()
    if not trimmed:
        return False

    # SQLite accepts statements with or without trailing ';' via Python API.
    # Keep this permissive but reject clearly broken endings.
    return not trimmed.endswith(",")
