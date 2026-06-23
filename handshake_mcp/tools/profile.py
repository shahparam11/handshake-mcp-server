"""Student profile and uploaded-documents tools."""

from __future__ import annotations

from fastmcp import FastMCP

from ..client import api_get


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def hs_get_profile() -> dict:
        """Get your Handshake student profile.

        Returns name, school, major, graduation year, and account status.
        """
        return await api_get("/students/me")

    @mcp.tool()
    async def hs_get_documents() -> dict:
        """List your uploaded resumes, cover letters, and other documents.

        Use the returned document IDs when calling hs_apply to attach files.
        """
        return await api_get("/documents")
