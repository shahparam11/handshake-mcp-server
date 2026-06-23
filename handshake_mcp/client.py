"""Authenticated HTTP client for the Handshake internal API.

All requests attach the saved session cookies. POST / DELETE requests also
reflect the CSRF-TOKEN cookie back as the X-CSRF-Token header, satisfying
Handshake's double-submit CSRF protection.

Endpoint base: https://app.joinhandshake.com/api/v1/
Note: Handshake's internal API is undocumented. If an endpoint returns 404,
open browser DevTools on Handshake → Network tab to find the correct path.
"""

from typing import Any

import httpx

from .auth import load_cookies

BASE_URL = "https://app.joinhandshake.com"
API_BASE = f"{BASE_URL}/api/v1"

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://app.joinhandshake.com/",
    "Origin": "https://app.joinhandshake.com",
}


def make_client() -> httpx.AsyncClient:
    """Return an authenticated AsyncClient using saved session cookies."""
    cookies = load_cookies()
    headers = dict(_HEADERS)
    # Handshake uses the double-submit CSRF pattern: reflect the cookie value
    # back as a request header.
    csrf = cookies.get("CSRF-TOKEN") or cookies.get("csrf_token", "")
    if csrf:
        headers["X-CSRF-Token"] = csrf
    return httpx.AsyncClient(
        cookies=cookies,
        headers=headers,
        follow_redirects=True,
        timeout=30.0,
    )


async def api_get(path: str, params: dict | None = None) -> Any:
    async with make_client() as c:
        r = await c.get(f"{API_BASE}{path}", params=params)
        r.raise_for_status()
        return r.json()


async def api_post(path: str, body: dict | None = None) -> Any:
    async with make_client() as c:
        r = await c.post(f"{API_BASE}{path}", json=body or {})
        r.raise_for_status()
        return r.json() if r.content else {"ok": True}


async def api_delete(path: str) -> Any:
    async with make_client() as c:
        r = await c.delete(f"{API_BASE}{path}")
        r.raise_for_status()
        return r.json() if r.content else {"ok": True}
