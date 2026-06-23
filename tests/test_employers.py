"""Tests for employer tools."""

import httpx
import pytest
import respx

from handshake_mcp.tools import employers

BASE = "https://app.joinhandshake.com/api/v1"


@respx.mock
@pytest.mark.asyncio
async def test_search_employers_passes_query():
    route = respx.get(f"{BASE}/employers").mock(
        return_value=httpx.Response(200, json={"results": [{"id": 1, "name": "Acme"}]})
    )
    result = await employers.handle("hs_search_employers", {"query": "Acme"})
    assert route.called
    assert "query=Acme" in str(route.calls[0].request.url)
    assert result["results"][0]["name"] == "Acme"


@respx.mock
@pytest.mark.asyncio
async def test_get_employer_by_id():
    route = respx.get(f"{BASE}/employers/42").mock(
        return_value=httpx.Response(200, json={"id": 42, "name": "TechCorp"})
    )
    result = await employers.handle("hs_get_employer", {"employer_id": "42"})
    assert route.called
    assert result["id"] == 42
