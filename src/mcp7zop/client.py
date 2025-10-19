# encoding : utf-8

import asyncio
from fastmcp import Client, FastMCP
from fastmcp.client.transports import FastMCPTransport

# display the list of tools available in the MCP server
async def test_server(mcp: FastMCP):
    transport = FastMCPTransport(mcp=mcp)
    async with Client(transport=transport) as client:
        result = await client.list_tools()
        for tool in result:
            print("--------------------------------------------------------------------")
            print(f"'{tool.name}' : {tool.description}")
            print("")

# helper for running the test
def mcp_server_test(mcp: FastMCP):
    """
    execute the test for the MCP server.
    This function runs the test_server function in an event loop.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_server(mcp))
    loop.close()

