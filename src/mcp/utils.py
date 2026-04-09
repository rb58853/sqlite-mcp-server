from ..db_client.database_conn import DatabaseConnection
import json

CLIENTS_TABLE_NAME = "clientes"
QUERY_EXCLUDE_TABLES: list[str] = []

db = DatabaseConnection()
base_db_context: str = f"""
    The database on which the query should be made contains the following exact information in JSON format. Each table or column name below is exactly the name it has in the database and should be used in the generated SQL query:
    {json.dumps(db.get_tables_and_columns(exclude_tables=QUERY_EXCLUDE_TABLES))}
"""

clients_table_context: str = f"""
The database on which the query should be made contains the following exact information in JSON format. Each table or column name below is exactly the name it has in the database and the one that should be used in the generated SQL query:
{json.dumps(db.get_table(CLIENTS_TABLE_NAME))} \n\n
"""
