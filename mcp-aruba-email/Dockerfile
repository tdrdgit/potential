FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DATA_DIR=/data \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR /app

# Install dependencies first for better layer caching.
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --upgrade pip && pip install .

# Persist the OAuth token database across restarts.
VOLUME ["/data"]
EXPOSE 8000

# Run the Streamable HTTP MCP server.
CMD ["python", "-m", "aruba_email_mcp"]
