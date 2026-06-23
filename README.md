# handshake-mcp

An [MCP](https://modelcontextprotocol.io) server that gives Claude tools to interact with the [Handshake](https://joinhandshake.com) career portal — search jobs, track applications, research employers, and more.

## Tools

| Tool | Description |
|---|---|
| `hs_search_jobs` | Search by keyword, location, or job type |
| `hs_get_job` | Full job description, requirements, salary, deadline |
| `hs_apply` | Submit an application, attach resume/cover letter |
| `hs_save_job` / `hs_unsave_job` / `hs_get_saved_jobs` | Bookmark management |
| `hs_get_applications` / `hs_withdraw_application` | Application tracking |
| `hs_search_employers` / `hs_get_employer` | Company research |
| `hs_get_profile` | Your Handshake student profile |
| `hs_get_documents` | Uploaded resumes and cover letters |

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) — `pip install uv`

## Setup

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/handshake-mcp.git
cd handshake-mcp
uv sync
```

### 2. First-time login

```bash
uv run handshake-mcp --login
```

A Chromium browser opens. Log in to Handshake (SSO, email, or school login), wait until your dashboard loads, then press Enter in the terminal. Session cookies are saved to `~/.handshake-mcp/cookies.json`.

### 3. Register with Claude Code

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

## Usage examples

```
Search for software engineering internships in Atlanta:
  hs_search_jobs(query="software engineer", location="Atlanta, GA", job_types=["internship"])

Get full job description and check how to apply:
  hs_get_job(job_id="12345678")

Apply and attach your resume:
  hs_get_documents()  # find your resume's document ID
  hs_apply(job_id="12345678", document_ids=[42])

Check all pending applications:
  hs_get_applications(status="pending")
```

## Development

```bash
uv sync --extra dev
uv run pytest
```

## Project layout

```
src/handshake_mcp/
├── auth.py          # Playwright login + cookie storage
├── client.py        # Authenticated httpx client + api_get/post/delete helpers
├── server.py        # MCP Server wiring + entry point
└── tools/
    ├── jobs.py          # hs_search_jobs, hs_get_job, hs_apply, hs_save_job, ...
    ├── employers.py     # hs_search_employers, hs_get_employer
    ├── applications.py  # hs_get_applications, hs_withdraw_application
    └── profile.py       # hs_get_profile, hs_get_documents
```

## How it works

After login, browser cookies are saved to `~/.handshake-mcp/cookies.json`. All API calls use these cookies against Handshake's internal REST API at `app.joinhandshake.com/api/v1/`. CSRF protection uses the double-submit cookie pattern — the `CSRF-TOKEN` cookie value is reflected back as the `X-CSRF-Token` request header.

> **Note:** Handshake's internal API is undocumented and may change. If a tool returns a 404, open browser DevTools on Handshake → Network tab, locate the matching request, and update the path in the relevant `tools/*.py` file.

## Session refresh

When you see `Session expired` errors:

```bash
uv run handshake-mcp --login
```

## License

MIT — see [LICENSE](LICENSE).
