"""Tests for tool schema validity and dispatch routing."""

import pytest

from handshake_mcp import tools


def test_all_tools_have_unique_names():
    names = [t.name for t in tools.ALL_TOOLS]
    assert len(names) == len(set(names)), "Duplicate tool names detected"


def test_all_tools_have_descriptions():
    for tool in tools.ALL_TOOLS:
        assert tool.description, f"{tool.name!r} is missing a description"


def test_all_tools_are_registered_in_dispatcher():
    for tool in tools.ALL_TOOLS:
        assert tool.name in tools._HANDLERS, f"No handler registered for {tool.name!r}"


def test_tool_count():
    assert len(tools.ALL_TOOLS) == 12


@pytest.mark.asyncio
async def test_dispatch_unknown_tool_raises():
    with pytest.raises(ValueError, match="Unknown tool"):
        await tools.dispatch("not_a_real_tool", {})
