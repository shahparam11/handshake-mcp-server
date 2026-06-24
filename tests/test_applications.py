"""Tests for application API calls."""

import httpx
import pytest
import respx

from handshake_mcp.client import api_post, gql

GQL = "https://app.joinhandshake.com/hs/graphql"
REST = "https://app.joinhandshake.com/stu"

_MOCK_APPS = {
    "totalCount": 2,
    "nodes": [
        {"id": "1", "status": "pending", "createdAt": "2026-01-01T00:00:00Z", "updatedAt": "2026-01-01T00:00:00Z"},
        {"id": "2", "status": "accepted", "createdAt": "2026-01-02T00:00:00Z", "updatedAt": "2026-01-03T00:00:00Z"},
    ],
}


@respx.mock
@pytest.mark.asyncio
async def test_get_applications_calls_graphql():
    route = respx.post(GQL).mock(
        return_value=httpx.Response(200, json={"data": {"currentUser": {"applications": _MOCK_APPS}}})
    )
    data = await gql("{ currentUser { applications { totalCount nodes { id status } } } }")
    assert route.called
    assert data["currentUser"]["applications"]["totalCount"] == 2


@respx.mock
@pytest.mark.asyncio
async def test_get_applications_returns_nodes():
    route = respx.post(GQL).mock(
        return_value=httpx.Response(200, json={"data": {"currentUser": {"applications": _MOCK_APPS}}})
    )
    data = await gql("{ currentUser { applications { nodes { id status } } } }")
    assert route.called
    assert data["currentUser"]["applications"]["nodes"][0]["status"] == "pending"


@respx.mock
@pytest.mark.asyncio
async def test_withdraw_application():
    route = respx.post(f"{REST}/applications/77/withdraw").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    await api_post("/applications/77/withdraw")
    assert route.called
