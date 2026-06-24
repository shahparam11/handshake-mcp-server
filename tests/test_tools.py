"""Tests for FastMCP server and tool registration."""

import asyncio

from handshake_mcp.server import create_mcp_server


def _get_tool_names() -> set[str]:
    mcp = create_mcp_server()
    tools = asyncio.run(mcp.list_tools())
    return {t.name for t in tools}


def test_server_creates_without_error():
    mcp = create_mcp_server()
    assert mcp is not None


def test_server_has_expected_tool_count():
    # 6 job tools + 2 employer + 2 application + 2 profile = 12
    assert len(_get_tool_names()) == 12


def test_all_tool_names_are_prefixed_hs():
    for name in _get_tool_names():
        assert name.startswith("hs_"), f"Tool {name!r} does not start with 'hs_'"


def test_expected_tools_are_registered():
    expected = {
        "hs_search_jobs",
        "hs_get_job",
        "hs_apply",
        "hs_save_job",
        "hs_unsave_job",
        "hs_get_saved_jobs",
        "hs_search_employers",
        "hs_get_employer",
        "hs_get_applications",
        "hs_withdraw_application",
        "hs_get_profile",
        "hs_get_documents",
    }
    assert _get_tool_names() == expected
