"""Console entrypoint: run the server over Streamable HTTP."""

from __future__ import annotations

from .server import build_mcp


def main() -> None:
    mcp = build_mcp()
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
