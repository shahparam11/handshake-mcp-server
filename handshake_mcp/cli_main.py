"""Command-line entry point for the Handshake MCP server.

Usage:
  handshake-mcp              # start MCP server (stdio)
  handshake-mcp --login      # authenticate via browser
  handshake-mcp --logout     # clear saved session
  handshake-mcp --status     # check session validity
  handshake-mcp --version    # print version
"""

import asyncio
import sys

from . import __version__
from .auth import run_login, run_logout, run_status
from .server import create_mcp_server


def main() -> None:
    args = set(sys.argv[1:])

    if "--version" in args or "-v" in args:
        print(f"handshake-mcp {__version__}")
        return

    if "--login" in args:
        asyncio.run(run_login())
        return

    if "--logout" in args:
        asyncio.run(run_logout())
        return

    if "--status" in args:
        asyncio.run(run_status())
        return

    mcp = create_mcp_server()
    mcp.run()
