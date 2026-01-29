import os
from pathlib import Path
from mcp import StdioServerParameters
from .base_client import StdioMCPClient

class FilesystemMCPClient(StdioMCPClient):
    def __init__(self, *, server_name: str | None = None, root_path: str | None = None):
        if root_path is None:
            resolved_path = str(Path.home().expanduser().resolve())
        else:
            resolved_path = str(Path(root_path).expanduser().resolve())
            if not Path.exists(Path(resolved_path)):
                raise ValueError(f"Provided root_path does not exist: {root_path}")
        
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", resolved_path],
            env=os.environ.copy(),
            cwd=os.getcwd(),
        )
        
        super().__init__(server_params, server_name)