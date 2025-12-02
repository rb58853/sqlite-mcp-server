from mcp.server.fastmcp import FastMCP
from . import Tools, Prompts, Resources

sqlite_mcp_server: FastMCP = FastMCP(name="sqlite_mcp_server", stateless_http=False)

Tools().registry(sqlite_mcp_server)
Prompts().registry(sqlite_mcp_server)
Resources().registry(sqlite_mcp_server)
