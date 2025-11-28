import contextlib
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel


class FastAppSettings(BaseModel):
    expose_url: str = "http://127.0.0.1:8000"
    """Public Expose IP"""
    dns: str = ""
    """Public Expose DNS"""
    # servers: list[FastMCP] = []
    # """MCP server that will be add to app"""


class FastAPP:
    def __init__(
        self,
        fast_app_settings: FastAppSettings = FastAppSettings(),
        servers: list[FastMCP] = [],
    ):
        self.app_settings: FastAppSettings = fast_app_settings
        self.servers = servers

    @property
    def app(self) -> FastAPI:
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

        return _app
