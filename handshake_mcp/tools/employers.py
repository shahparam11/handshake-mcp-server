"""Employer search and company profile tools."""

from __future__ import annotations

from fastmcp import FastMCP

from ..client import gql

_EMPLOYER_FIELDS = """
  id
  name
  description
  website
  location { name }
  industry { name }
"""

_SEARCH_QUERY = """
query SearchEmployers($limit: Int) {
  employers(limit: $limit) {
    """ + _EMPLOYER_FIELDS + """
  }
}
"""

_GET_EMPLOYER_QUERY = """
query GetEmployer($id: ID!) {
  employer(id: $id) {
    """ + _EMPLOYER_FIELDS + """
  }
}
"""


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def hs_search_employers(limit: int = 25) -> dict:
        """Browse employers on Handshake.

        Returns employers visible to your account. Use hs_get_employer
        for full details on a specific company.

        Args:
            limit: Number of employers to return (max 100).
        """
        data = await gql(_SEARCH_QUERY, {"limit": min(limit, 100)})
        return {"employers": data["employers"]}

    @mcp.tool()
    async def hs_get_employer(employer_id: str) -> dict:
        """Get a company's Handshake profile.

        Includes description, industry, location, and website.

        Args:
            employer_id: Employer ID from hs_search_employers results.
        """
        data = await gql(_GET_EMPLOYER_QUERY, {"id": employer_id})
        return data["employer"]
