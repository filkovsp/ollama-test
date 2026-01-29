this package provides "Client" implementation as shown here:
https://pypi.org/project/langchain-mcp-adapters/

an alternative to the client classes could be approach with Multiple MCP Servers
see link above and the same also documented here:
https://reference.langchain.com/python/langchain_mcp_adapters

code example:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main() -> None:
  filesystem_mcp_params = {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:/temp"],
      "env": os.environ.copy(),
      "transport": "stdio",
  }
  
  git_mcp_params = {
      "command": sys.executable,
      "args": ["-m", "mcp_server_git"],
      "env": os.environ.copy(),
      "transport": "stdio",
  }
  mcp_client = MultiServerMCPClient({
      "filesystem": filesystem_mcp_params,
      "git": git_mcp_params
  })

  async with mcp_client.session("git"), mcp_client.session("filesystem"):
    try:
      git_tools = await mcp_client.get_tools(server_name="git")
      filesystem_tools = await mcp_client.get_tools(server_name="filesystem")
      
      # call original MCP Tool:
      # from datetime import timedelta
      # await mcp_client.session("filesystem").call_tool(name="list_directory", arguments={"path": "D:/temp"}, read_timeout_seconds=timedelta(seconds=27))

      all_tool = git_tools + filesystem_tools

      print(f"Available tools:", *all_tool, sep="\n")
    except Exception as e:
      print("oops....", e)
```