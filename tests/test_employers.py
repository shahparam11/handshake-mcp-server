"""Tests for employer API calls."""

import httpx
import pytest
import respx

from handshake_mcp.client import api_get

BASE = "https://app.joinhandshake.com/api/v1"


@respx.mock
@pytest.mark.asyncio
async def test_search_employers_passes_query():
    route = respx.get(f"{BASE}/employers").mock(
        return_value=httpx.Response(200, json={"results": [{"id": 1, "name": "Acme"}]})
    )
    result = await api_get("/employers", {"query": "Acme"})
    assert route.called
    assert "query=Acme" in str(route.calls[0].request.url)
    assert result["results"][0]["name"] == "Acme"


@respx.mock
@pytest.mark.asyncio
async def test_get_employer_by_id():
    route = respx.get(f"{BASE}/employers/42").mock(
        return_value=httpx.Response(200, json={"id": 42, "name": "TechCorp"})
    )
    result = await api_get("/employers/42")
    assert route.called
    assert result["id"] == 42
