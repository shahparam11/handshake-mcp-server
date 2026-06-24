"""Tests for job-related API calls."""

import json

import httpx
import pytest
import respx

from handshake_mcp.client import api_delete, api_post, gql

GQL = "https://app.joinhandshake.com/hs/graphql"
REST = "https://app.joinhandshake.com/stu"

_MOCK_JOB = {
    "id": "12345",
    "title": "SWE Intern",
    "description": "Build cool stuff.",
    "remote": False,
    "employer": {"id": "99", "name": "Acme", "website": None, "location": {"name": "SF"}, "industry": {"name": "Tech"}},
    "jobType": {"name": "Internship"},
    "employmentType": {"name": "Part-Time"},
    "salaryType": {"name": "Paid"},
    "createdAt": "2026-01-01T00:00:00Z",
    "startDate": None,
}


@respx.mock
@pytest.mark.asyncio
async def test_search_jobs_calls_graphql():
    nodes = [{"job": _MOCK_JOB}]
    route = respx.post(GQL).mock(
        return_value=httpx.Response(200, json={"data": {"jobSearch": {"totalCount": 1, "nodes": nodes}}})
    )
    data = await gql("{ jobSearch(first: 5) { totalCount nodes { job { id title } } } }")
    assert route.called
    assert data["jobSearch"]["totalCount"] == 1


@respx.mock
@pytest.mark.asyncio
async def test_get_job_by_id():
    route = respx.post(GQL).mock(
        return_value=httpx.Response(200, json={"data": {"job": _MOCK_JOB}})
    )
    data = await gql("query GetJob($id: ID!) { job(id: $id) { id title } }", {"id": "12345"})
    assert route.called
    assert data["job"]["id"] == "12345"


@respx.mock
@pytest.mark.asyncio
async def test_apply_sends_document_ids():
    route = respx.post(f"{REST}/postings/99/apply").mock(
        return_value=httpx.Response(201, json={"status": "submitted"})
    )
    await api_post("/postings/99/apply", {"document_ids": [7, 8]})
    assert route.called
    body = json.loads(route.calls[0].request.content)
    assert body == {"document_ids": [7, 8]}


@respx.mock
@pytest.mark.asyncio
async def test_save_job_posts_posting_id():
    route = respx.post(f"{REST}/saved_jobs").mock(
        return_value=httpx.Response(201, json={"id": 55, "posting_id": 12345})
    )
    await api_post("/saved_jobs", {"posting_id": 12345})
    assert route.called
    body = json.loads(route.calls[0].request.content)
    assert body["posting_id"] == 12345


@respx.mock
@pytest.mark.asyncio
async def test_unsave_job_deletes():
    route = respx.delete(f"{REST}/saved_jobs/55").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    await api_delete("/saved_jobs/55")
    assert route.called
