# encoding : utf-8

import argparse
from .server import get_mcp
from .client import mcp_server_test
from fastmcp import FastMCP

# MCPサーバーとして動作させる
def run_as_mcp_server(mcp: FastMCP):
    # MCPサーバーを起動
    mcp.run(transport="stdio")

# メイン関数
def main():
    parser = argparse.ArgumentParser(description="Run MCP server")
    parser.add_argument(
        "-server",
        "--mcp-server",
        action="store_true",
        help="Run as MCP server",
    )
    args = parser.parse_args()

    mcp = get_mcp()
    if args.mcp_server:
        run_as_mcp_server(mcp=mcp)
    else:
        mcp_server_test(mcp=mcp)

# main
if __name__ == "__main__":
    main()
