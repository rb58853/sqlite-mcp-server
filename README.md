# SQLite MCP Server

Este repositorio representa un Servidor MCP especializado en realizar consultas y otras operaciones sobre una base de datos SQL.

## Run Servers

### Httpstream MCP Server

```shell
python3.x src/main.py --host 127.0.0.1 --port 8080 --mode http-stream
```

## Client Usage

Como cliente para consumir este servidor MCP se usa el proyecto del repositorio [TalRepo](https://github.com/rb58853/fastchat-mcp). Siga los pasos del readme del mismo para conectarse con este servidor.

### Client Configuration

- `Headers`:

    ``` json
    { "MASTER-TOKEN": "your `.env` master token" } 
    ```

- `Transfer Protocol`: httpstream
- `Url`: "expose_api_dns_or_http_url+port/sqlite_mcp_server/mcp"

> **Note:**  Es importante qu el nombre de los headers sea exactamente el que se proporciona. `✅MASTER-TOKEN` | `❌MASTER_TOKEN`

### Example config for [`Fastchat-mcp`](https://github.com/rb58853/fastchat-mcp) client

```json
{
    "mcp_servers": {
        "sqlite_server": {
            "protocol": "httpstream",
            "httpstream-url": "http://127.0.0.1:8080/sqlite_mcp_server/mcp",
            "name": "sqlite_server",
            "description": "This server specializes in sqlite operations.",
            "headers": {
                "MASTER-TOKEN": "<your master token>"
            }
        }
    }
}
```

## Database SQL Connection

La conexion la base de datos SQL requiere que se le pase la direccion de la bas de datos `.db`. En caso de no pasarse una direccion absoluta de la base de datos, entonces se usara como dababase el archivo `"path/to/root_folder/daabase/data/sample.db"`.

### Environment

Para usar una direccion absoluta de la base de datos se debe poner la misma en el environment:

```.env
# Path to database .db (If not set this env var then Path will be "project_root/database/data/example/db")
DATABASE_ABSOLUTE_PATH=/path/to/database.db
```

### Creacion automatica de ejemplo

Para crear una base de datos de ejemplo, se puede ejecutar el archivo `database/create_sample_db.py` dentro de este proyecto. Este deberia crear una base de datos sqlite de ejemplo en el archivo `database/data/sample.db`. Este archivo depende de la biblioteca `sqlite3`.

```shell
python3 database/create_sample_db.py
```
