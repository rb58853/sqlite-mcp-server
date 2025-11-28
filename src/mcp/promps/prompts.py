import json
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import UserMessage, Message
from ...config.logger import logger
from ...db_client.database_conn import DatabaseConnection

db = DatabaseConnection._instance


class Prompts:
    def registry(self, mcp: FastMCP):
        @mcp.prompt(
            description=f"""
            Genera un prompt para explicar al LLM todo el contexto de la base de datos sqlite que se tiene. 
            Devuelve informacion detallada dada como contexto adicional al LLM.
            Este prompt se debe llamar siempre que se quera hacer una consulta a la base de datos y requieras mas contexto que el general de tablas y datos generales.
            Si basta con la informacion de tablas y datos propocionados entonces no debe usarse este prompt. Pero si es necesario mas contexto que el dado a continuacion, entonces este prompt debe llamarse y pasarlo al LLM.
            Data General:
            {json.dumps(db.get_tables_and_columns())}
            """
        )
        def explain_context_prompt() -> list[Message]:
            data: dict = {}
            prompt_text = f"""
            A continuacion se muestra la estructura e informacion Detallada de algunos campos y datos de la base de datos proporcionada: 
            {json.dumps(data)}
            """

            logger.debug(f"Generated describe_query_prompt text: {prompt_text}")
            result = [UserMessage(prompt_text)]
            logger.debug("Exiting describe_query_prompt()")
            return result
