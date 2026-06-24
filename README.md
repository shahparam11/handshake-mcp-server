# handshake-mcp

An [MCP](https://modelcontextprotocol.io) server that gives AI assistants like Claude access to [Handshake](https://joinhandshake.com) — search jobs, apply, track applications, and research employers through your own browser session.

> **Disclaimer:** This project is independent and unaffiliated with Handshake. Automated access may violate Handshake's Terms of Service. Use for personal productivity only.

## Tools

| Tool | Description |
|---|---|
| `hs_search_jobs` | Search by keyword, location, or job type |
| `hs_get_job` | Full description, requirements, salary, deadline |
| `hs_apply` | Submit an application, attach resume/cover letter |
| `hs_save_job` / `hs_unsave_job` / `hs_get_saved_jobs` | Bookmark management |
| `hs_get_applications` / `hs_withdraw_application` | Application tracking |
| `hs_search_employers` / `hs_get_employer` | Company research |
| `hs_get_profile` | Your Handshake student profile |
| `hs_get_documents` | Uploaded resumes and cover letters |

## Quick start

### With uvx (recommended)

```bash
# First-time login
uvx handshake-mcp --login

# Add to Claude Code (~/.claude/.mcp.json)
```

```json
{
  "mcpServers": {
    "handshake": {
      "command": "uvx",
      "args": ["handshake-mcp"]
    }
  }
}
```

### From source

```bash
git clone https://github.com/shahparam11/handshake-mcp-server.git
cd handshake-mcp
uv sync

# First-time login
uv run handshake-mcp --login
```

Add to `~/.claude/.mcp.json`:

```json
{
  "mcpServers": {
    "handshake": {
      "command": "uv",
      "args": ["run", "--project", "/path/to/handshake-mcp", "handshake-mcp"]
    }
  }
}
```

Restart Claude Code. The `hs_*` tools are now available.

### With Docker

```bash
docker build -t handshake-mcp .

# Login (mounts session storage)
docker run -it -v ~/.handshake-mcp:/root/.handshake-mcp handshake-mcp --login

# Run as MCP server
docker run -i -v ~/.handshake-mcp:/root/.handshake-mcp handshake-mcp
```

## CLI

```bash
handshake-mcp --login    # authenticate via browser
handshake-mcp --status   # check session validity
handshake-mcp --logout   # clear saved session
handshake-mcp --version  # print version
```

## How it works

On `--login`, a Patchright Chromium browser opens. After you log in, the full browser profile (cookies, localStorage, IndexedDB) is saved to `~/.handshake-mcp/`. Subsequent tool calls use these cookies via an `httpx` client against Handshake's internal REST API at `app.joinhandshake.com/stu/`.

CSRF protection uses the **double-submit cookie** pattern — the `CSRF-TOKEN` cookie value is reflected back as the `X-CSRF-Token` request header.

> **Note:** Handshake's internal API is undocumented. If a tool returns 404, open browser DevTools on Handshake → Network tab, find the matching request path, and update the relevant `handshake_mcp/tools/*.py` file.

## Session refresh

```bash
handshake-mcp --login
```

## Project layout

```
handshake_mcp/
├── cli_main.py       # Entry point — --login/--logout/--status/server
├── server.py         # FastMCP server factory
├── auth.py           # Patchright login + profile/cookie storage
├── client.py         # Authenticated httpx client
├── exceptions.py     # CredentialsNotFoundError, SessionExpiredError
└── tools/
    ├── jobs.py           # hs_search_jobs, hs_get_job, hs_apply, hs_save/unsave/get_saved_jobs
    ├── employers.py      # hs_search_employers, hs_get_employer
    ├── applications.py   # hs_get_applications, hs_withdraw_application
    └── profile.py        # hs_get_profile, hs_get_documents
```

## Development

```bash
uv sync --group dev
uv run pytest --cov
uv run ruff check .
```

## License

MIT — see [LICENSE](LICENSE).
