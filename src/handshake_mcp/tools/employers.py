"""Employer search and company profile tools."""

from typing import Any

from mcp.types import Tool

from ..client import api_get

TOOLS: list[Tool] = [
    Tool(
        name="hs_search_employers",
        description="Search for companies/employers on Handshake by name or keyword.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Company name or industry keyword",
                },
                "page": {"type": "integer", "default": 1},
                "per_page": {"type": "integer", "default": 25},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="hs_get_employer",
        description=(
            "Get a company's Handshake profile: description, industry, "
            "employee count, open job count, and active postings."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "employer_id": {
                    "type": "string",
                    "description": "Employer ID (from hs_search_employers)",
                },
            },
            "required": ["employer_id"],
        },
    ),
]


async def handle(name: str, args: dict) -> Any:
    match name:
        case "hs_search_employers":
            return await api_get(
                "/employers",
                {
                    "query": args["query"],
                    "page": args.get("page", 1),
                    "per_page": args.get("per_page", 25),
                },
            )

        case "hs_get_employer":
            return await api_get(f"/employers/{args['employer_id']}")

        case _:
            raise ValueError(f"Unrouted tool in employers module: {name!r}")
