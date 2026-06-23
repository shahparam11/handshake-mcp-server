"""Tests for FastMCP server and tool registration."""

from handshake_mcp.server import create_mcp_server


def test_server_creates_without_error():
    mcp = create_mcp_server()
    assert mcp is not None


def test_server_has_expected_tool_count():
    mcp = create_mcp_server()
    # 6 job tools + 2 employer + 2 application + 2 profile = 12
    assert len(mcp._tool_manager._tools) == 12


def test_all_tool_names_are_prefixed_hs():
    mcp = create_mcp_server()
    for name in mcp._tool_manager._tools:
        assert name.startswith("hs_"), f"Tool {name!r} does not start with 'hs_'"


def test_expected_tools_are_registered():
    mcp = create_mcp_server()
    tools = set(mcp._tool_manager._tools.keys())
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
    assert tools == expected
