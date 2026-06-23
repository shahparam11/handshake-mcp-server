FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies first (layer cache)
COPY pyproject.toml ./
RUN uv sync --no-dev --no-install-project

# Install Patchright Chromium
RUN uv run patchright install chromium --with-deps

# Copy source
COPY handshake_mcp/ ./handshake_mcp/

# Session storage — mount ~/.handshake-mcp from host to persist login
VOLUME ["/root/.handshake-mcp"]

ENTRYPOINT ["uv", "run", "handshake-mcp"]
