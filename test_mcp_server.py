from __future__ import print_function
import asyncio
from mcp_use import MCPClient

from dotenv import load_dotenv
load_dotenv()  # Loads from .env file


async def main() -> None:
    # https://mcp-use.com/docs/python/client/client-configuration
    # https://mcp-use.com/docs/python/client/direct-tool-calls
    
    mcp_config = {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:/temp"]
            }
        }
    }

    client = MCPClient(config = mcp_config)
    
    try:
        await client.create_all_sessions()
        await asyncio.sleep(0.25) # add some timeout to allow seesion initialize
        
        session = client.get_session("filesystem")
        tools = await session.list_tools()
        
        tool_names = [t.name for t in tools]
        print(f"Available tools:", *tool_names, sep="\n")
        
        # Call a specific tool with arguments
        result = await session.call_tool(
            name="list_directory",
            arguments={"path": "D:/temp"}
        )

        # Handle the result
        if getattr(result, "isError", False):
            print(f"Error: {result.content}")
        else:
            # print(f"Tool result: {result.content}")
            print(f"Text result (text): {result.content[0].text}")
    
    except Exception as e:
        print("oops, error:", e)

    finally:
        await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())