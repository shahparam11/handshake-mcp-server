"""Aggregates all tool definitions and dispatches calls to the right module."""

from collections.abc import Awaitable, Callable
from typing import Any

from mcp.types import Tool

from . import applications, employers, jobs, profile

ALL_TOOLS: list[Tool] = (
    jobs.TOOLS
    + employers.TOOLS
    + applications.TOOLS
    + profile.TOOLS
)

_HANDLERS: dict[str, Callable[[str, dict], Awaitable[Any]]] = {
    **{t.name: jobs.handle for t in jobs.TOOLS},
    **{t.name: employers.handle for t in employers.TOOLS},
    **{t.name: applications.handle for t in applications.TOOLS},
    **{t.name: profile.handle for t in profile.TOOLS},
}


async def dispatch(name: str, args: dict) -> Any:
    handler = _HANDLERS.get(name)
    if not handler:
        raise ValueError(f"Unknown tool: {name!r}")
    return await handler(name, args)
