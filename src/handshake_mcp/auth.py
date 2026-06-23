"""Cookie-based authentication for Handshake.

Login flow: open a visible Chromium window, let the user log in normally,
then save all resulting cookies to COOKIES_FILE. Subsequent API calls
attach those cookies to every request.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

HANDSHAKE_DIR = Path.home() / ".handshake-mcp"
COOKIES_FILE = HANDSHAKE_DIR / "cookies.json"


def load_cookies() -> dict[str, str]:
    """Return saved session cookies as a name→value dict.

    Raises RuntimeError if the user has not run --login yet.
    """
    if not COOKIES_FILE.exists():
        raise RuntimeError(
            "Not logged in to Handshake.\n"
            "Run:  handshake-mcp --login\n"
            "      (or: uv run handshake-mcp --login)"
        )
    with open(COOKIES_FILE) as f:
        data = json.load(f)
    # Playwright stores cookies as a list of {name, value, domain, ...} dicts.
    if isinstance(data, list):
        return {c["name"]: c["value"] for c in data}
    return data


async def run_login() -> None:
    """Open a headed Chromium browser so the user can log in, then save cookies."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("playwright not found — installing...")
        os.system(f'"{sys.executable}" -m pip install playwright')
        os.system("playwright install chromium")
        from playwright.async_api import async_playwright

    HANDSHAKE_DIR.mkdir(parents=True, exist_ok=True)

    print()
    print("╔══════════════════════════════════════════════╗")
    print("║        Handshake MCP — First-time Login      ║")
    print("╚══════════════════════════════════════════════╝")
    print()
    print("Steps:")
    print("  1. A browser will open — log in to Handshake.")
    print("  2. Wait until your dashboard / job feed loads.")
    print("  3. Come back here and press Enter.")
    print()

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False, slow_mo=200)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        page = await ctx.new_page()
        await page.goto(
            "https://app.joinhandshake.com/login",
            wait_until="domcontentloaded",
        )

        input(">>> Press Enter after you are fully logged in to Handshake... ")

        cookies = await ctx.cookies(["https://app.joinhandshake.com"])
        await browser.close()

    if not cookies:
        print("\nNo cookies captured — login may have failed. Try again.")
        sys.exit(1)

    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f, indent=2)

    print(f"\nSaved {len(cookies)} cookies → {COOKIES_FILE}")
    print("Restart Claude Code to activate the Handshake MCP server.")
