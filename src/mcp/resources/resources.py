import json
from mcp.server.fastmcp import FastMCP
from ...config.logger import logger
from ...db_client.database_conn import DatabaseConnection

db = DatabaseConnection._instance

class Resources:
    def registry(self, mcp: FastMCP):
        pass
        # @mcp.resource("schema://sqlite/all")
        # def list_table_schemas() -> str:
        #     """
        #     Retrieve the schemas for all tables in the database in JSON format.

        #     Returns:
        #         A JSON-formatted string mapping table names to their SQL schema.
        #     """
        #     logger.debug("Entering list_table_schemas()")
        #     try:
        #         # Get all tables from sqlite_master where type is table.
        #         cursor = db.connection.execute(
        #             "SELECT name, sql FROM sqlite_master WHERE type='table'"
        #         )
        #         rows = cursor.fetchall()
        #         # Build a dictionary: table name -> schema SQL.
        #         schemas = {row["name"]: row["sql"] for row in rows if row["sql"]}
        #         result = json.dumps(schemas, indent=2)
        #         logger.debug(f"Retrieved table schemas: {schemas}")
        #     except Exception as e:
        #         result = f"Error retrieving table schemas: {e}"
        #         logger.exception(result)
        #     logger.debug("Exiting list_table_schemas()")
        #     return result
