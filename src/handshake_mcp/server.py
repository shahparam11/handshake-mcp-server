"""MCP server entry point.

Wires together the tool registry and handles the MCP protocol.
Run with --login to perform the one-time Playwright browser login.
"""

import asyncio
import json
import sys

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent

from . import tools
from .auth import run_login

_server = Server("handshake")


@_server.list_tools()
async def list_tools() -> list:
    return tools.ALL_TOOLS


@_server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = await tools.dispatch(name, arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        body = e.response.text[:600]
        msg = f"Handshake API error {status}: {body}"
        if status == 401:
            msg += "\n\nSession expired — re-run: handshake-mcp --login"
        elif status == 403:
            msg += "\n\nForbidden — CSRF token may be stale. Re-login to refresh."
        return [TextContent(type="text", text=msg)]
    except RuntimeError as e:
        return [TextContent(type="text", text=str(e))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error ({type(e).__name__}): {e}")]


def main() -> None:
    if "--login" in sys.argv:
        asyncio.run(run_login())
    else:
        asyncio.run(stdio_server(_server))
