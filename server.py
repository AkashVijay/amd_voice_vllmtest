from fastmcp import FastMCP
import asyncio
import os
import argparse
from mcp_tools.arxiv_tools import initialize_tools
from mcp_tools.prompts import check_prompts
from db.models import Base, engine

Base.metadata.create_all(engine)
mcp = FastMCP("Arxiv server", port=8008)

initialize_tools(mcp)
check_prompts(mcp)

# @mcp.tool()
# def hello_world(name: str = "World"):
#     """A simple hello world tool."""
#     return {"message": f"Hello, {name}!"}

# @mcp.tool()
# def add(a: int, b: int):
#     """Add two numbers."""
#     return a + b

if __name__ == "__main__":
    print("Starting MCP server on default port...")
    mcp.run()

# mcpo --port 8008 -- python server.py
# mcpo --port 8004 -- npx -y @smithery/cli@latest run  @mikechao/balldontlie-mcp --profile characteristic-cephalopod-ovaZ4Q --key 09c2cabe-9c5d-4245-8a68-10951a7c1572
# mcpo --port 8007 -- npx -y @smithery/cli@latest run mcp-simple-arxiv --key 09c2cabe-9c5d-4245-8a68-10951a7c1572