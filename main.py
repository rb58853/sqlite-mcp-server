import click
import asyncio
from fastapi import FastAPI
from uvicorn import Config, Server

from src.api.httpstream import FastAPP, FastAppSettings
from src.mcp.server import sqlite_mcp_server
from src.config.logger import logger


def httpstream(port: int, host: str, dns):
    """
    Start and run the MCP HTTP stream server.

    This function configures a FastAPI application using FastAppSettings and the
    provided MCP server, then starts an asynchronous Uvicorn server using
    asyncio.run. It logs the server address when starting.

    Parameters
    ----------
    port : int
        TCP port to bind the server to (e.g., 8080).
    host : str
        Host address to bind the server to (e.g., "0.0.0.0" or "0.0.0.0").
    dns : str | None
        Optional DNS name under which the server is exposed. If None, an empty
        DNS value is used in the application settings.

    """
    
    settings: FastAppSettings = FastAppSettings(
        dns="" if dns is None else dns,
        expose_url=f"http://{host}:{port}",
    )

    httpstream_api: FastAPI = FastAPP(
        fast_app_settings=settings, servers=[sqlite_mcp_server]
    ).app

    async def run_server() -> None:
        config = Config(
            httpstream_api,
            host=host,
            port=port,
            log_level="info",
        )
        server = Server(config)

        logger.info(f"🚀 MCP Httpstream Server running on http://{host}:{port}")
        await server.serve()

    asyncio.run(run_server())


@click.command()
@click.option("--port", default=8080, help="Port to listen on")
@click.option("--host", default="0.0.0.0", help="Host to hosted on")
@click.option("--mode", default="http-stream", help="Hoted Mode")
@click.option(
    "--dns",
    default=None,
    type=str,
    help="DNS en el cual se expone el servidor. Default: None",
)
def main(port: int, host: str, mode: str, dns: str | None):
    if mode == "http-stream":
        httpstream(port=port, host=host, dns=dns)


if __name__ == "__main__":
    main()
