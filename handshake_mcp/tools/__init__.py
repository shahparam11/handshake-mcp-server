"""Tool registration for the Handshake MCP server."""

from fastmcp import FastMCP

from . import applications, employers, jobs, profile


def register_all(mcp: FastMCP) -> None:
    """Register every tool group with the FastMCP server instance."""
    jobs.register(mcp)
    employers.register(mcp)
    applications.register(mcp)
    profile.register(mcp)
