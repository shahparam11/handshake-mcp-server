"""Student profile and uploaded-documents tools."""

from __future__ import annotations

from fastmcp import FastMCP

from ..client import gql

_PROFILE_QUERY = """
{
  currentUser {
    id
    name
    firstName
    lastName
    bio
    headline
    graduationDate
    school { name }
  }
}
"""

_DOCUMENTS_QUERY = """
{
  currentUser {
    documents {
      id
      name
      createdAt
    }
  }
}
"""


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def hs_get_profile() -> dict:
        """Get your Handshake student profile.

        Returns name, school, bio, headline, and graduation date.
        """
        data = await gql(_PROFILE_QUERY)
        return data["currentUser"]

    @mcp.tool()
    async def hs_get_documents() -> dict:
        """List your uploaded resumes, cover letters, and other documents.

        Use the returned document IDs when calling hs_apply to attach files.
        """
        data = await gql(_DOCUMENTS_QUERY)
        return data["currentUser"]["documents"]
