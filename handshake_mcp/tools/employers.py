"""Employer search and company profile tools."""

from __future__ import annotations

from fastmcp import FastMCP

from ..client import api_get


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def hs_search_employers(
        query: str,
        page: int = 1,
        per_page: int = 25,
    ) -> dict:
        """Search for companies/employers on Handshake.

        Args:
            query: Company name or industry keyword.
            page: Page number (starts at 1).
            per_page: Results per page.
        """
        return await api_get(
            "/employers",
            {"query": query, "page": page, "per_page": per_page},
        )

    @mcp.tool()
    async def hs_get_employer(employer_id: str) -> dict:
        """Get a company's Handshake profile.

        Includes description, industry, employee count, open job count,
        and active postings.

        Args:
            employer_id: Employer ID from hs_search_employers results.
        """
        return await api_get(f"/employers/{employer_id}")
