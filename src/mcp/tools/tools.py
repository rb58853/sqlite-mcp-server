import json
from mcp.server.fastmcp import FastMCP
from ...config.logger import logger
from ...db_client.database_conn import DatabaseConnection

db = DatabaseConnection()


class Tools:
    def registry(self, mcp: FastMCP):
        @mcp.tool(
            description=f"""
            Execute a read-only SQL query. Only SELECT statements are allowed. 
            Para cualquier informacion relacionada con la empresa o con la base de datos, si esta informacion puede estar contenida en los datos de la misma, se debe llamar esta herramienta pasandole una consulta SQL con el objetivo de recuperar la informacion que se pide.
            La base de datos sobre la cual se debe hacer la query cuenta con la siguiente informacion exacta en formato JSON. Cada nombre de tabla o columna a continuacion es exactamente el nomre que tiene en la base de datos y el que debe usarse en la query SQL generada:
            {json.dumps(db.get_tables_and_columns())}

            Args:
                query: The SQL query to execute.

            Returns:
                A JSON-formatted string containing query results or an error message.
            """
        )
        def sql_query(query: str) -> str:
            logger.debug(f"Entering sql_query() with query: {query}")

            # Basic safety check: enforce that only SELECT queries are permitted.
            if not query.strip().lower().startswith("select"):
                msg = "Error: Only SELECT queries are allowed."
                logger.warning(f"Query rejected: {query}. {msg}")
                return msg

            try:
                # Execute the query.
                cursor = db.connection.execute(query)
                # Convert the resulting rows into a list of dictionaries for serialization.
                rows = [dict(row) for row in cursor.fetchall()]
                result = json.dumps(rows, indent=2)
                logger.debug(f"SQL query executed successfully. Result: {result}")
            except Exception as e:
                result = f"Error executing query: {e}"
                logger.exception(result)

            logger.debug("Exiting sql_query()")
            return result
