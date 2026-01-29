import os
import sys
from mcp import StdioServerParameters
from .base_client import StdioMCPClient

class GitMCPClient(StdioMCPClient):
    def __init__(self, *, server_name: str | None = None):
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_server_git"],
            env=os.environ.copy(),
            cwd=os.getcwd(),
        )
        super().__init__(server_params, server_name)