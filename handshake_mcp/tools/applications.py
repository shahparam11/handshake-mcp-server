"""Application tracking and withdrawal tools."""

from __future__ import annotations

from fastmcp import FastMCP

from ..client import api_post, gql

_APPLICATIONS_QUERY = """
{
  currentUser {
    applications {
      totalCount
      nodes {
        id
        status
        createdAt
        updatedAt
      }
    }
  }
}
"""


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def hs_get_applications() -> dict:
        """List all your Handshake job applications with their current status.

        Returns application ID, status, and timestamps. Statuses include:
        pending, accepted, declined, withdrawn, interview.
        """
        data = await gql(_APPLICATIONS_QUERY)
        return data["currentUser"]["applications"]

    @mcp.tool()
    async def hs_withdraw_application(application_id: str) -> dict:
        """Withdraw a submitted Handshake job application.

        Args:
            application_id: Application ID from hs_get_applications.
        """
        return await api_post(f"/applications/{application_id}/withdraw")
