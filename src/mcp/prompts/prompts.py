from mcp.server.fastmcp import FastMCP
from ...db_client.database_conn import DatabaseConnection

class Prompts:
    """Prompts Registry for MCP"""
    def __init__(self):
        self.db = DatabaseConnection()

    def registry(self, mcp: FastMCP):
        # Fill with your custom Prompts
        pass
