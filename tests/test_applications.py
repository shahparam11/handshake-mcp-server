"""Tests for application tools."""

import httpx
import pytest
import respx

from handshake_mcp.tools import applications

BASE = "https://app.joinhandshake.com/api/v1"


@respx.mock
@pytest.mark.asyncio
async def test_get_applications_no_filter():
    route = respx.get(f"{BASE}/job_applications").mock(
        return_value=httpx.Response(200, json={"results": [], "total": 0})
    )
    await applications.handle("hs_get_applications", {})
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_get_applications_with_status_filter():
    route = respx.get(f"{BASE}/job_applications").mock(
        return_value=httpx.Response(200, json={"results": [], "total": 0})
    )
    await applications.handle("hs_get_applications", {"status": "pending"})
    assert "status=pending" in str(route.calls[0].request.url)


@respx.mock
@pytest.mark.asyncio
async def test_withdraw_application():
    route = respx.post(f"{BASE}/job_applications/77/withdraw").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    await applications.handle("hs_withdraw_application", {"application_id": "77"})
    assert route.called
