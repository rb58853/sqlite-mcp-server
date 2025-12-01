# SQLite MCP Server

A lightweight FastAPI-based server exposing one or more FastMCP instances for read-only (SELECT) SQL queries against a SQLite database. It implements simple token-based authentication and strict policies to prevent schema or data modifications.[web:1][web:5]

## Purpose

The server hosts tools enabling SELECT-only queries on SQLite databases. It enforces secure access and token-based authentication via MASTER_TOKEN.[web:7]

## Quick Start

### Local Python Setup

1. Install dependencies using the project's `requirements.txt`.
2. Configure environment variables (see [Configuration](#configuration-and-environment-variables) section).
3. Generate a sample database using [`database/create_sample_db.py`]() or connect to a custom database via `.env`.

4. Launch the HTTP-stream server:

    ```bash
    python3 -m src.main --mode http-stream --host 0.0.0.0 --port 8080
    ```

### Docker Deployment

Deploy a Docker container with the sample database using Docker Compose.

``` bash
```

## General Architecture

- `src/main.py`: CLI entry point; constructs `FastAppSettings` and mounts configured MCP servers.
- `src/api/httpstream/api.py`: Builds the FastAPI application; manages FastMCP session lifecycles; mounts each FastMCP server at `/{server.name}`; provides root redirection to `/help` and exposes URLs via `/help` endpoint; integrates [Fastauth](https://github.com/rb58853/fastauth-api) middleware using `MASTER_TOKEN`.[web:3]
- `src/mcp/tools/tools.py`: Loads YAML descriptions and registers MCP tools: `sql_query` (generic SELECT-only), `clients_sql_query` (SELECT-only for `clientes` table); base implementation (`base_sql_query`) executes queries and returns JSON.
- `src/mcp/utils.py`: Generates contextual prompts and DB schema JSON fragments: `base_db_context` (tables/columns schema, excluding `clientes`); `clients_table_context` (schema for `clientes` table).
- `src/mcp/tools/descriptions/query_tools.yaml`: Human/machine descriptions for LLM-generated SQL tools; enforces single SELECT statements without modifications or external execution.[web:7]

## Configuration and Environment Variables

- `MASTER_TOKEN` (required): Authenticates clients via `MASTER-TOKEN` header (case-sensitive).
- `DATABASE_ABSOLUTE_PATH` (optional): Absolute path to `.db` file; defaults to repository sample database.
- CLI options (`src/main.py`): `--host`, `--port`, `--mode` (e.g., `http-stream`), `--dns` (optional public value for `/help`).

## Authentication and Security

[Fastauth](https://github.com/rb58853/fastauth-api) middleware validates requests using `MASTER_TOKEN`. Tools enforce SQL statements starting with `SELECT` (case-insensitive); non-SELECT queries are rejected. YAML descriptions mandate single SELECT, no DDL/DML, no transactions, no external execution. Execution returns JSON-serialized rows; errors are logged and returned as strings.[web:5]

## Database Management

### DatabaseConnection

- Establishes SQLite connections.
- `get_tables_and_columns(exclude_tables=...)` generates JSON schemas.
- `get_table(name)` retrieves table schemas (e.g., `clientes`).

### Sample Database Creation

Execute `database/create_sample_db.py` to create `database/data/sample.db` using `sqlite3`.



```shell
python3 database/create_sample_db.py
```


## Client Example ([fastchat-mcp](https://github.com/rb58853/fastchat-mcp) Configuration)

Adjust host/port/name and replace token:

```json
{
    "mcp_servers": {
        "sqlite_server_example": {
            "protocol": "httpstream",
            "httpstream-url": "http://127.0.0.1:8080/sqlite_mcp_server/mcp",
            "name": "sqlite_server_example",
            "description": "SQLite MCP for read-only SQL tools",
            "headers": {
                "MASTER-TOKEN": "<tu_master_token_aqui>"
            }
        }
    }
}
```

## Tool Registration and Query Execution

Tools load YAML from `src/mcp/tools/descriptions` and register with FastMCP, attaching contexts (`base_db_context` or `clients_table_context`). `base_sql_query` validates SELECT prefix, executes via `db.connection.execute(query)`, converts to dictionaries, and returns formatted JSON; errors yield messages and logs. `clients_sql_query` prepends `clientes` table context for precise LLM schema awareness.[web:1]

## Logging and Debugging

Configured logger (`src/config/logger`) handles debug/error messages. SQL execution errors include tracebacks in logs; API returns descriptive strings.[web:3]

## Useful Paths

- CLI entry: `src/main.py`
- FastAPI factory: `src/api/httpstream/api.py`
- MCP tool loader: `src/mcp/tools/tools.py`
- DB context helpers: `src/mcp/utils.py`
- SQL tool descriptions: `src/mcp/tools/descriptions/query_tools.yaml`

## Considerations

The SQL data extraction implementation is generic yet adaptable. While generalization excels, large datasets may confuse LLMs; separating tools (e.g., `clientes` from generic queries) enhances comprehension via dedicated resources like `get_clients_data(query:str)`. This decouples code, isolates dependencies, and supports specialized MCPs (e.g., clients-only with separate databases). Future extensions benefit from such separations for precise LLM tool/resource contexts.