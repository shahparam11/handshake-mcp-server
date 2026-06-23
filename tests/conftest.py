"""Shared test fixtures."""

import pytest


@pytest.fixture(autouse=True)
def fake_cookies(monkeypatch):
    """Patch load_cookies so tests never need a real Handshake session."""
    monkeypatch.setattr(
        "handshake_mcp.client.load_cookies",
        lambda: {
            "_handshake_session": "test-session-token",
            "CSRF-TOKEN": "test-csrf-token",
        },
    )
