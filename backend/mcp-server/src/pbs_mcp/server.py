"""MCP stdio server — entry point for the pbs-bureau backend.

Spawned by Claude Code via the .mcp.json registration. Communicates
over stdio with the MCP protocol. All tool surface is registered
here; implementations live in pbs_mcp.tools.*.
"""
from __future__ import annotations

import asyncio
import logging
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

logger = logging.getLogger("pbs_mcp")

server: Server = Server("pbs-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Return the registered tool surface.

    v0.1: scaffolding only. Tools wired in subsequent commits.
    """
    return []


async def _run() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")
    logger.info("pbs-mcp starting")
    asyncio.run(_run())


if __name__ == "__main__":
    main()
