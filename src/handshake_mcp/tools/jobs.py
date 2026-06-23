"""Job search, details, apply, and save/unsave tools."""

from typing import Any

from mcp.types import Tool

from ..client import api_delete, api_get, api_post

TOOLS: list[Tool] = [
    Tool(
        name="hs_search_jobs",
        description=(
            "Search for jobs and internships on Handshake. "
            "Returns posting ID, title, employer, location, type, and deadline. "
            "Pass the posting ID to hs_get_job for the full description."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keywords, job title, or company name",
                },
                "location": {
                    "type": "string",
                    "description": "City/state or 'Remote'",
                },
                "job_types": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "full_time",
                            "part_time",
                            "internship",
                            "co_op",
                            "fellowship",
                            "volunteer",
                        ],
                    },
                    "description": "Filter by job type (omit for all types)",
                },
                "page": {"type": "integer", "default": 1, "minimum": 1},
                "per_page": {"type": "integer", "default": 20, "maximum": 50},
            },
        },
    ),
    Tool(
        name="hs_get_job",
        description=(
            "Get full details of a Handshake job posting: "
            "description, requirements, salary, deadline, and application method."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "job_id": {
                    "type": "string",
                    "description": "Handshake posting ID (from hs_search_jobs)",
                },
            },
            "required": ["job_id"],
        },
    ),
    Tool(
        name="hs_apply",
        description=(
            "Submit a Handshake application for a job. "
            "Call hs_get_job first to confirm the application method — "
            "external-apply jobs redirect to the employer's own site."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "job_id": {
                    "type": "string",
                    "description": "Handshake posting ID",
                },
                "document_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": (
                        "IDs of documents to attach (resume, cover letter). "
                        "Get IDs with hs_get_documents."
                    ),
                },
            },
            "required": ["job_id"],
        },
    ),
    Tool(
        name="hs_save_job",
        description="Bookmark a Handshake job posting to your saved-jobs list.",
        inputSchema={
            "type": "object",
            "properties": {
                "job_id": {
                    "type": "string",
                    "description": "Handshake posting ID",
                },
            },
            "required": ["job_id"],
        },
    ),
    Tool(
        name="hs_unsave_job",
        description="Remove a job from your Handshake saved-jobs list.",
        inputSchema={
            "type": "object",
            "properties": {
                "saved_job_id": {
                    "type": "string",
                    "description": (
                        "Saved-job record ID (from hs_get_saved_jobs). "
                        "This is different from the posting ID."
                    ),
                },
            },
            "required": ["saved_job_id"],
        },
    ),
    Tool(
        name="hs_get_saved_jobs",
        description="List all jobs you have bookmarked on Handshake.",
        inputSchema={
            "type": "object",
            "properties": {
                "page": {"type": "integer", "default": 1},
                "per_page": {"type": "integer", "default": 25},
            },
        },
    ),
]


async def handle(name: str, args: dict) -> Any:
    match name:
        case "hs_search_jobs":
            params: dict[str, Any] = {
                "page": args.get("page", 1),
                "per_page": args.get("per_page", 20),
            }
            if args.get("query"):
                params["query"] = args["query"]
            if args.get("location"):
                params["location"] = args["location"]
            # Rails array param style: job_types[]=full_time&job_types[]=internship
            for jt in args.get("job_types", []):
                params.setdefault("job_types[]", []).append(jt)
            return await api_get("/postings", params)

        case "hs_get_job":
            return await api_get(f"/postings/{args['job_id']}")

        case "hs_apply":
            body: dict[str, Any] = {}
            if args.get("document_ids"):
                body["document_ids"] = args["document_ids"]
            return await api_post(f"/postings/{args['job_id']}/apply", body)

        case "hs_save_job":
            return await api_post("/saved_jobs", {"posting_id": int(args["job_id"])})

        case "hs_unsave_job":
            return await api_delete(f"/saved_jobs/{args['saved_job_id']}")

        case "hs_get_saved_jobs":
            return await api_get(
                "/saved_jobs",
                {"page": args.get("page", 1), "per_page": args.get("per_page", 25)},
            )

        case _:
            raise ValueError(f"Unrouted tool in jobs module: {name!r}")
