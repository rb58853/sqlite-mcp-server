import yaml
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from ...config.logger import logger
from ...db_client.database_conn import DatabaseConnection

CLIENTS_TABLE_NAME = "clientes"
QUERY_EXCLUDE_TABLES: list[str] = [CLIENTS_TABLE_NAME]

"""
Lista de tablas de la base de datos que seran excluidas de la generacion base de consulta SQL.
"""


class Tools:
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

    # TODO: Cambiar estas properties que no son properties. Llevarlas a un archivo independiente encargado solo del prompting
    @property
    def __base_db_context(self) -> str:
        return f"""
        ## Database Context
        Para cualquier informacion relacionada con la empresa o con la base de datos, solo si esta informacion puede estar contenida en los datos de la misma, se debe llamar esta herramienta pasandole una consulta SQL con el objetivo de recuperar la informacion que se pide. La base de datos sobre la cual se debe hacer la query cuenta con la siguiente informacion exacta en formato JSON. Cada nombre de tabla o columna a continuacion es exactamente el nomre que tiene en la base de datos y el que debe usarse en la query SQL generada:
        {json.dumps(self.db.get_tables_and_columns(exclude_tables=QUERY_EXCLUDE_TABLES))} 
        \n\n Solo sebe usarse este servicio si el usuario pide datos que se encuentren en estas tablas \n\n
        """

    @property
    def __clients_table_context(self):
        return f"""
        ## Database Context
        Para cualquier informacion relacionada con los clientes si esta informacion puede estar contenida los datos de la tabla clientes que se pasa, se debe llamar esta herramienta pasandole una consulta SQL con el objetivo de recuperar la informacion que se pide del usuario o de los usuarios. La base de datos sobre la cual se debe hacer la query cuenta con la siguiente informacion exacta en formato JSON. Cada nombre de tabla o columna a continuacion es exactamente el nomre que tiene en la base de datos y el que debe usarse en la query SQL generada:
        {json.dumps(self.db.get_table(CLIENTS_TABLE_NAME))} \n\n
        """

    ###########################################################################################################################################
    def __get_description(self, tool_name: str) -> str:
        return self.__base_db_context + self.descriptions.get(tool_name, "")

    def registry(self, mcp: FastMCP) -> None:
        @mcp.tool(description=self.__get_description(tool_name="sql_query"))
        def sql_query(query: str) -> str:
            base_sql_query(query=query, db=self.db)

        @mcp.tool(
            description=self.__clients_table_context
            + self.descriptions.get("clients_sql_query", "")
        )
        def clients_sql_query(query: str) -> str:
            base_sql_query(query=query, db=self.db)


def base_sql_query(query: str, db: DatabaseConnection) -> str:
    """
    Funcion encargada de realizar consultas SQL
    """
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
