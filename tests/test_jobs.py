"""Tests for job API calls."""

import json

import httpx
import pytest
import respx

from handshake_mcp.client import api_delete, api_get, api_post

BASE = "https://app.joinhandshake.com/api/v1"


@respx.mock
@pytest.mark.asyncio
async def test_search_jobs_calls_postings():
    route = respx.get(f"{BASE}/postings").mock(
        return_value=httpx.Response(200, json={"results": [], "total": 0})
    )
    result = await api_get("/postings", {"query": "software engineer", "page": 1})
    assert route.called
    assert result["total"] == 0


@respx.mock
@pytest.mark.asyncio
async def test_get_job_by_id():
    route = respx.get(f"{BASE}/postings/12345").mock(
        return_value=httpx.Response(200, json={"id": 12345, "title": "SWE Intern"})
    )
    result = await api_get("/postings/12345")
    assert route.called
    assert result["id"] == 12345


@respx.mock
@pytest.mark.asyncio
async def test_apply_sends_document_ids():
    route = respx.post(f"{BASE}/postings/99/apply").mock(
        return_value=httpx.Response(201, json={"status": "submitted"})
    )
    await api_post("/postings/99/apply", {"document_ids": [7, 8]})
    assert route.called
    body = json.loads(route.calls[0].request.content)
    assert body == {"document_ids": [7, 8]}


@respx.mock
@pytest.mark.asyncio
async def test_save_job_posts_posting_id():
    route = respx.post(f"{BASE}/saved_jobs").mock(
        return_value=httpx.Response(201, json={"id": 55, "posting_id": 12345})
    )
    await api_post("/saved_jobs", {"posting_id": 12345})
    assert route.called
    body = json.loads(route.calls[0].request.content)
    assert body["posting_id"] == 12345


@respx.mock
@pytest.mark.asyncio
async def test_unsave_job_deletes():
    route = respx.delete(f"{BASE}/saved_jobs/55").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    await api_delete("/saved_jobs/55")
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_get_saved_jobs():
    route = respx.get(f"{BASE}/saved_jobs").mock(
        return_value=httpx.Response(200, json={"results": [], "total": 0})
    )
    await api_get("/saved_jobs", {"page": 1, "per_page": 25})
    assert route.called
