"""Custom exceptions for the Handshake MCP server."""


class CredentialsNotFoundError(RuntimeError):
    """Raised when no valid Handshake session is found on disk."""

    def __init__(self) -> None:
        super().__init__(
            "Not logged in to Handshake.\n"
            "Run one of:\n"
            "  handshake-mcp --login\n"
            "  uv run handshake-mcp --login\n"
            "  uvx handshake-mcp --login\n\n"
            "A browser will open — log in, then press Enter."
        )


class SessionExpiredError(RuntimeError):
    """Raised when the saved session cookies are no longer valid."""

    def __init__(self) -> None:
        super().__init__(
            "Handshake session expired.\n"
            "Re-run:  handshake-mcp --login"
        )
