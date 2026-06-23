"""Tests for job tools."""

import json

import httpx
import pytest
import respx

from handshake_mcp.tools import jobs

BASE = "https://app.joinhandshake.com/api/v1"


@respx.mock
@pytest.mark.asyncio
async def test_search_jobs_calls_postings_endpoint():
    route = respx.get(f"{BASE}/postings").mock(
        return_value=httpx.Response(200, json={"results": [], "total": 0})
    )
    result = await jobs.handle("hs_search_jobs", {"query": "software engineer"})
    assert route.called
    assert result == {"results": [], "total": 0}


@respx.mock
@pytest.mark.asyncio
async def test_search_jobs_passes_location():
    route = respx.get(f"{BASE}/postings").mock(
        return_value=httpx.Response(200, json={"results": []})
    )
    await jobs.handle("hs_search_jobs", {"query": "SWE", "location": "Atlanta, GA"})
    url = str(route.calls[0].request.url)
    assert "location=Atlanta" in url


@respx.mock
@pytest.mark.asyncio
async def test_get_job_fetches_by_id():
    route = respx.get(f"{BASE}/postings/12345").mock(
        return_value=httpx.Response(200, json={"id": 12345, "title": "SWE Intern"})
    )
    result = await jobs.handle("hs_get_job", {"job_id": "12345"})
    assert route.called
    assert result["id"] == 12345


@respx.mock
@pytest.mark.asyncio
async def test_apply_posts_to_correct_path():
    route = respx.post(f"{BASE}/postings/99/apply").mock(
        return_value=httpx.Response(201, json={"status": "submitted"})
    )
    result = await jobs.handle("hs_apply", {"job_id": "99", "document_ids": [7, 8]})
    assert route.called
    body = json.loads(route.calls[0].request.content)
    assert body == {"document_ids": [7, 8]}


@respx.mock
@pytest.mark.asyncio
async def test_save_job_posts_posting_id():
    route = respx.post(f"{BASE}/saved_jobs").mock(
        return_value=httpx.Response(201, json={"id": 55, "posting_id": 12345})
    )
    await jobs.handle("hs_save_job", {"job_id": "12345"})
    assert route.called
    body = json.loads(route.calls[0].request.content)
    assert body == {"posting_id": 12345}


@respx.mock
@pytest.mark.asyncio
async def test_unsave_job_deletes_correct_record():
    route = respx.delete(f"{BASE}/saved_jobs/55").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    await jobs.handle("hs_unsave_job", {"saved_job_id": "55"})
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_get_saved_jobs():
    route = respx.get(f"{BASE}/saved_jobs").mock(
        return_value=httpx.Response(200, json={"results": [], "total": 0})
    )
    await jobs.handle("hs_get_saved_jobs", {})
    assert route.called
