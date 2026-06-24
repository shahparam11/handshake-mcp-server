"""Tests for employer API calls."""

import httpx
import pytest
import respx

from handshake_mcp.client import gql

GQL = "https://app.joinhandshake.com/hs/graphql"

_MOCK_EMPLOYER = {
    "id": "42",
    "name": "TechCorp",
    "description": "We build things.",
    "website": "https://techcorp.example",
    "location": {"name": "San Francisco, CA"},
    "industry": {"name": "Software"},
}


@respx.mock
@pytest.mark.asyncio
async def test_search_employers_calls_graphql():
    route = respx.post(GQL).mock(
        return_value=httpx.Response(200, json={"data": {"employers": [_MOCK_EMPLOYER]}})
    )
    data = await gql("query SearchEmployers($limit: Int) { employers(limit: $limit) { id name } }", {"limit": 5})
    assert route.called
    assert data["employers"][0]["name"] == "TechCorp"


@respx.mock
@pytest.mark.asyncio
async def test_get_employer_by_id():
    route = respx.post(GQL).mock(
        return_value=httpx.Response(200, json={"data": {"employer": _MOCK_EMPLOYER}})
    )
    data = await gql("query GetEmployer($id: ID!) { employer(id: $id) { id name } }", {"id": "42"})
    assert route.called
    assert data["employer"]["id"] == "42"
