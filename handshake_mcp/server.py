"""FastMCP server factory for the Handshake MCP server."""

from fastmcp import FastMCP

from .tools import register_all


def create_mcp_server() -> FastMCP:
    mcp = FastMCP(
        name="Handshake",
        instructions=(
            "Interact with the Handshake career portal. "
            "Available capabilities: search jobs and internships, view full job details, "
            "apply to positions, bookmark and manage saved jobs, track application status, "
            "research employers, and access your student profile and uploaded documents. "
            "All tools are prefixed with 'hs_'. "
            "Tip: call hs_get_job before hs_apply to verify the application method."
        ),
    )
    register_all(mcp)
    return mcp
