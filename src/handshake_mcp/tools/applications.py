"""Application tracking and withdrawal tools."""

from typing import Any

from mcp.types import Tool

from ..client import api_get, api_post

TOOLS: list[Tool] = [
    Tool(
        name="hs_get_applications",
        description=(
            "List all your Handshake job applications with status "
            "(pending, accepted, declined, withdrawn, interview)."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "page": {"type": "integer", "default": 1},
                "per_page": {"type": "integer", "default": 25},
                "status": {
                    "type": "string",
                    "enum": [
                        "pending",
                        "accepted",
                        "declined",
                        "withdrawn",
                        "interview",
                    ],
                    "description": "Filter by status (omit for all applications)",
                },
            },
        },
    ),
    Tool(
        name="hs_withdraw_application",
        description="Withdraw a submitted Handshake job application.",
        inputSchema={
            "type": "object",
            "properties": {
                "application_id": {
                    "type": "string",
                    "description": "Application ID (from hs_get_applications)",
                },
            },
            "required": ["application_id"],
        },
    ),
]


async def handle(name: str, args: dict) -> Any:
    match name:
        case "hs_get_applications":
            params: dict[str, Any] = {
                "page": args.get("page", 1),
                "per_page": args.get("per_page", 25),
            }
            if args.get("status"):
                params["status"] = args["status"]
            return await api_get("/job_applications", params)

        case "hs_withdraw_application":
            return await api_post(
                f"/job_applications/{args['application_id']}/withdraw"
            )

        case _:
            raise ValueError(f"Unrouted tool in applications module: {name!r}")
