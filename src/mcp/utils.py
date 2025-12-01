from ..db_client.database_conn import DatabaseConnection
import json

CLIENTS_TABLE_NAME = "clientes"
QUERY_EXCLUDE_TABLES: list[str] = [CLIENTS_TABLE_NAME]

db = DatabaseConnection()
base_db_context: str = f"""
    For any information related to the company or the database, only if this information can be contained in the database data, this tool should be called by passing an SQL query with the aim of retrieving the requested information. The database on which the query should be made contains the following exact information in JSON format. Each table or column name below is exactly the name it has in the database and should be used in the generated SQL query:
    {json.dumps(db.get_tables_and_columns(exclude_tables=QUERY_EXCLUDE_TABLES))}
    \n\n This service should only be used if the user requests data found in these tables \n\n
"""

clients_table_context: str = f"""
For any information related to clients, if this information can be contained in the data from the clients table provided, this tool should be called by passing an SQL query with the objective of retrieving the information requested by the user or users. The database on which the query should be made contains the following exact information in JSON format. Each table or column name below is exactly the name it has in the database and the one that should be used in the generated SQL query:
{json.dumps(db.get_table(CLIENTS_TABLE_NAME))} \n\n
"""
