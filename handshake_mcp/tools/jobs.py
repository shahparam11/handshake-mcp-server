"""Job search, details, apply, and bookmark tools."""

from __future__ import annotations

from fastmcp import FastMCP

from ..client import api_delete, api_get, api_post


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def hs_search_jobs(
        query: str = "",
        location: str = "",
        job_types: list[str] | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> dict:
        """Search for jobs and internships on Handshake.

        Returns posting ID, title, employer, location, type, and deadline.
        Pass the posting ID to hs_get_job for the full description.

        Args:
            query: Keywords, job title, or company name.
            location: City/state or 'Remote'.
            job_types: Filter by type — full_time, part_time, internship,
                co_op, fellowship, volunteer. Omit for all types.
            page: Page number (starts at 1).
            per_page: Results per page (max 50).
        """
        params: dict = {"page": page, "per_page": min(per_page, 50)}
        if query:
            params["query"] = query
        if location:
            params["location"] = location
        for jt in job_types or []:
            params.setdefault("job_types[]", []).append(jt)
        return await api_get("/postings", params)

    @mcp.tool()
    async def hs_get_job(job_id: str) -> dict:
        """Get full details of a Handshake job posting.

        Includes description, requirements, salary, application deadline,
        and application_method (handshake | external).

        Args:
            job_id: Handshake posting ID (from hs_search_jobs results).
        """
        return await api_get(f"/postings/{job_id}")

    @mcp.tool()
    async def hs_apply(
        job_id: str,
        document_ids: list[int] | None = None,
    ) -> dict:
        """Submit a Handshake application for a job.

        Call hs_get_job first to confirm the application_method field —
        external-apply jobs redirect to the employer's own site and cannot
        be submitted here.

        Args:
            job_id: Handshake posting ID.
            document_ids: IDs of documents to attach (resume, cover letter).
                Retrieve IDs with hs_get_documents.
        """
        body: dict = {}
        if document_ids:
            body["document_ids"] = document_ids
        return await api_post(f"/postings/{job_id}/apply", body)

    @mcp.tool()
    async def hs_save_job(job_id: str) -> dict:
        """Bookmark a job posting to your Handshake saved-jobs list.

        Args:
            job_id: Handshake posting ID.
        """
        return await api_post("/saved_jobs", {"posting_id": int(job_id)})

    @mcp.tool()
    async def hs_unsave_job(saved_job_id: str) -> dict:
        """Remove a job from your Handshake saved-jobs list.

        Args:
            saved_job_id: Saved-job record ID from hs_get_saved_jobs.
                This is different from the posting ID.
        """
        return await api_delete(f"/saved_jobs/{saved_job_id}")

    @mcp.tool()
    async def hs_get_saved_jobs(page: int = 1, per_page: int = 25) -> dict:
        """List all jobs you have bookmarked on Handshake.

        Args:
            page: Page number (starts at 1).
            per_page: Results per page.
        """
        return await api_get("/saved_jobs", {"page": page, "per_page": per_page})
