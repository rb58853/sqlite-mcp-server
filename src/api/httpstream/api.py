import contextlib
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastauth import Fastauth, FastauthSettings
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import os


class FastAppSettings(BaseModel):
    expose_url: str = "http://0.0.0.0:8000"
    """Public Expose IP"""
    dns: str = ""
    """Public Expose DNS"""


class FastAPP:
    """
    ## FastAPP
    High-level manager that builds a FastAPI application exposing one or more FastMCP
    servers with coordinated lifecycle management and simple authentication.
    Responsibilities:
    - Manage asynchronous lifespan of all provided FastMCP session managers so they
        are started and stopped with the application.
    - Mount each FastMCP HTTP app under "/{server.name}".
    - Provide a root redirect ("/") to a small help endpoint ("/help") that lists
        available servers and basic client information.
    - Apply Fastauth middleware using environment-provided `MASTER_TOKEN` and
        cryptography key for simple authorization.
    Attributes:
            app_settings (FastAppSettings): Application configuration (e.g. expose_url).
            servers (list[FastMCP]): Sequence of FastMCP instances to expose and manage.
    ## Properties
            app -> FastAPI: Constructed and configured FastAPI application. Creating
            this property wires up lifespan management, mounts server apps, registers
            the redirect/help endpoints, and attaches Fastauth middleware.
    ## Usage notes:
    - The `Fastauth` master token and cryptography key are read from the
        `MASTER_TOKEN` environment variable by default.
    - Server mount paths are derived from each server's name; spaces are replaced
        with underscores in help URLs.
    """

    def __init__(
        self,
        fast_app_settings: FastAppSettings = FastAppSettings(),
        servers: list[FastMCP] = [],
    ):
        """
        Initialize the API instance.
        Args:
            fast_app_settings (FastAppSettings): Application configuration to use. Defaults to a new FastAppSettings().
            servers (list[FastMCP], optional): List of FastMCP server instances to manage. Defaults to an empty list.
        """
        self.app_settings: FastAppSettings = fast_app_settings
        self.servers = servers

    @property
    def app(self) -> FastAPI:
        """Create and configure the FastAPI application for the MCP servers.
        Builds and returns a FastAPI instance that:
        - Manages the asynchronous lifespan of all server session managers.
        - Mounts each FastMCP's HTTP app at `"/{server.name}"`.
        - Registers a root redirect (`"/"`) and a `"/help"` JSON endpoint describing servers.
        - Applies Fastauth middleware using `MASTER_TOKEN` (and cryptography key) from env.
        Returns:
            FastAPI: A configured FastAPI application ready to be served.
        """

        # servers: list[FastMCP] = self.app_settings.servers
        servers: list[FastMCP] = self.servers

        # Create a combined lifespan to manage both session managers
        @contextlib.asynccontextmanager
        async def lifespan(app: FastAPI):
            async with contextlib.AsyncExitStack() as stack:
                for server in servers:
                    await stack.enter_async_context(server.session_manager.run())
                yield

        _app = FastAPI(lifespan=lifespan)
        for server in servers:
            _app.mount(f"/{server.name}", server.streamable_http_app())

        @_app.get("/", include_in_schema=False)
        async def redirect_to_help():
            return RedirectResponse(url="/help")

        @_app.get("/help", include_in_schema=False)
        async def help():
            return {
                "mcp_servers": [
                    f"{self.app_settings.expose_url}/{server.name.replace(' ','_')}/mcp"
                    for server in self.servers
                ],
                "doc": "",
                "client_example": "https://github.com/rb58853/fastchat-mcp",
            }

        # Set simple middleware authorization
        # See fastauth documentation https://github.com/rb58853/fastauth-api
        auth_settings: FastauthSettings = FastauthSettings(
            app_name="sqlite mcp server",
            database_api_path=None,
            master_token=os.getenv("MASTER_TOKEN"),
            cryptography_key=os.getenv("MASTER_TOKEN"),
            master_token_paths=["/sqlite_mcp_server"],
        )
        auth = Fastauth(settings=auth_settings)
        auth.set_auth(_app)
        _app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=[
                "77.237.243.163",
                "77.237.243.163:8080",
                "http://77.237.243.163:8080",
                "localhost",
                "0.0.0.0",
                "127.0.0.1",
            ],
        )
        #####################################################################
        return _app
