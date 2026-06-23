"""Application tracking and withdrawal tools."""

from __future__ import annotations

from fastmcp import FastMCP

from ..client import api_get, api_post


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def hs_get_applications(
        page: int = 1,
        per_page: int = 25,
        status: str | None = None,
    ) -> dict:
        """List all your Handshake job applications with their current status.

        Statuses: pending, accepted, declined, withdrawn, interview.

        Args:
            page: Page number (starts at 1).
            per_page: Results per page.
            status: Filter by status — omit to return all applications.
        """
        params: dict = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        return await api_get("/job_applications", params)

    @mcp.tool()
    async def hs_withdraw_application(application_id: str) -> dict:
        """Withdraw a submitted Handshake job application.

        Args:
            application_id: Application ID from hs_get_applications.
        """
        return await api_post(f"/job_applications/{application_id}/withdraw")
