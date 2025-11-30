import json
import yaml
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from ...config.logger import logger
from ...db_client.database_conn import DatabaseConnection

db = DatabaseConnection()

CLIENTS_TABLE_NAME: str = "clientes"

class Resources:
    def __init__(self):
        self.db = DatabaseConnection()
        # db_tables_and_columns: dict = db.get_tables_and_columns()
        self.descriptions: dict[str:str] = {}
        self.__load_descriptions()

    def __load_descriptions(self) -> None:
        """Load tool descriptions from YAML files."""
        # Path to the descriptions directory
        descriptions_dir = Path(__file__).parent / "descriptions"

        # Check if the directory exists
        if not descriptions_dir.exists():
            raise FileNotFoundError(
                f"Tool descriptions directory not found: {descriptions_dir}"
            )

        # Load all YAML files in the directory
        for yaml_file in descriptions_dir.glob("*.yaml"):
            try:
                with open(yaml_file) as f:
                    tool_descriptions = yaml.safe_load(f)
                    if tool_descriptions:
                        self.descriptions.update(tool_descriptions)
            except Exception as e:
                print(f"Error loading tool descriptions from {yaml_file}: {e}")

   
    def registry(self, mcp: FastMCP):
        pass