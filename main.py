import click
import asyncio
from fastapi import FastAPI
from uvicorn import Config, Server

from src.api.httpstream.api import FastAPP, FastAppSettings
from src.mcp.server import sqlite_mcp_server
from src.config.logger import logger

def httpstream(port: int, host: str, dns):
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
@click.option("--host", default="127.0.0.1", help="Host to hosted on")
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
