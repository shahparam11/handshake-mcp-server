"""Tests for application API calls."""

import httpx
import pytest
import respx

from handshake_mcp.client import api_get, api_post

BASE = "https://app.joinhandshake.com/api/v1"


@respx.mock
@pytest.mark.asyncio
async def test_get_applications_no_filter():
    route = respx.get(f"{BASE}/job_applications").mock(
        return_value=httpx.Response(200, json={"results": [], "total": 0})
    )
    await api_get("/job_applications", {"page": 1, "per_page": 25})
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_get_applications_with_status_filter():
    route = respx.get(f"{BASE}/job_applications").mock(
        return_value=httpx.Response(200, json={"results": [], "total": 0})
    )
    await api_get("/job_applications", {"page": 1, "per_page": 25, "status": "pending"})
    assert "status=pending" in str(route.calls[0].request.url)


@respx.mock
@pytest.mark.asyncio
async def test_withdraw_application():
    route = respx.post(f"{BASE}/job_applications/77/withdraw").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    await api_post("/job_applications/77/withdraw")
    assert route.called
