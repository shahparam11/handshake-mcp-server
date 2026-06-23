"""Student profile and uploaded documents tools."""

from typing import Any

from mcp.types import Tool

from ..client import api_get

TOOLS: list[Tool] = [
    Tool(
        name="hs_get_profile",
        description=(
            "Get your Handshake student profile: "
            "name, school, major, graduation year, and account status."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="hs_get_documents",
        description=(
            "List your uploaded resumes, cover letters, and other documents on Handshake. "
            "Use the returned document IDs when calling hs_apply."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
]


async def handle(name: str, args: dict) -> Any:
    match name:
        case "hs_get_profile":
            return await api_get("/students/me")

        case "hs_get_documents":
            return await api_get("/documents")

        case _:
            raise ValueError(f"Unrouted tool in profile module: {name!r}")
