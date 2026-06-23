"""Browser-based authentication for Handshake.

Uses Patchright (anti-detection Playwright fork) with a persistent browser
profile so the full session state — cookies, localStorage, IndexedDB — is
preserved between logins and survives Handshake's bot-detection checks.

Profile layout:
  ~/.handshake-mcp/
  ├── profile/          ← persistent Chromium user-data directory
  └── cookies.json      ← exported cookies snapshot (used by the httpx client)
"""

import json
import logging
import os
import shutil
import sys
from pathlib import Path

from .exceptions import CredentialsNotFoundError

logger = logging.getLogger(__name__)

HANDSHAKE_DIR = Path(os.environ.get("HANDSHAKE_DIR", Path.home() / ".handshake-mcp"))
PROFILE_DIR = HANDSHAKE_DIR / "profile"
COOKIES_FILE = HANDSHAKE_DIR / "cookies.json"

_LOGIN_URL = "https://app.joinhandshake.com/login"
_APP_ORIGIN = "https://app.joinhandshake.com"

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def load_cookies() -> dict[str, str]:
    """Return saved session cookies as {name: value}.

    Raises CredentialsNotFoundError if the user has not logged in yet.
    """
    if not COOKIES_FILE.exists():
        raise CredentialsNotFoundError()
    with open(COOKIES_FILE) as f:
        data = json.load(f)
    if isinstance(data, list):
        return {c["name"]: c["value"] for c in data}
    return data


async def run_login() -> None:
    """Open a headed Patchright browser, let the user log in, save the session."""
    try:
        from patchright.async_api import async_playwright
    except ImportError:
        print("patchright not found — installing...")
        os.system(f'"{sys.executable}" -m pip install patchright')
        os.system("patchright install chromium")
        from patchright.async_api import async_playwright

    HANDSHAKE_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    print()
    print("╔══════════════════════════════════════════════╗")
    print("║        Handshake MCP — Login                 ║")
    print("╚══════════════════════════════════════════════╝")
    print()
    print("Steps:")
    print("  1. A browser will open — log in to Handshake.")
    print("  2. Wait until your dashboard / job feed loads.")
    print("  3. Come back here and press Enter.")
    print()

    async with async_playwright() as pw:
        ctx = await pw.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            slow_mo=200,
            user_agent=_USER_AGENT,
            viewport={"width": 1280, "height": 800},
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        await page.goto(_LOGIN_URL, wait_until="domcontentloaded")

        input(">>> Press Enter after you are fully logged in to Handshake... ")

        cookies = await ctx.cookies([_APP_ORIGIN])
        await ctx.close()

    if not cookies:
        print("\nNo cookies captured — login may have failed. Try again.")
        sys.exit(1)

    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f, indent=2)

    print(f"\nSaved {len(cookies)} cookies → {COOKIES_FILE}")
    print("Restart Claude Code to activate the Handshake MCP server.")


async def run_logout() -> None:
    """Remove the saved session profile and cookies."""
    removed: list[str] = []
    if PROFILE_DIR.exists():
        shutil.rmtree(PROFILE_DIR)
        removed.append("profile/")
    if COOKIES_FILE.exists():
        COOKIES_FILE.unlink()
        removed.append("cookies.json")

    if removed:
        print(f"Removed: {', '.join(removed)}")
        print("Session cleared. Run --login to authenticate again.")
    else:
        print("No session found — nothing to remove.")


async def run_status() -> None:
    """Check whether the saved session is still valid."""
    if not COOKIES_FILE.exists():
        print("✗ Not logged in (no cookies.json found).")
        print("  Run:  handshake-mcp --login")
        return

    from .client import api_get

    try:
        data = await api_get("/students/me")
        name = (
            data.get("name")
            or f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
            or "unknown"
        )
        print(f"✓ Logged in as: {name}")
        if school := data.get("primary_education", {}).get("school", {}).get("name"):
            print(f"  School: {school}")
    except Exception as exc:
        print(f"✗ Session invalid: {exc}")
        print("  Re-run:  handshake-mcp --login")
