from contextlib import asynccontextmanager
from typing import AsyncIterator
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class StdioMCPClient:
    def __init__(self, server_params: StdioServerParameters, server_name: str = None, **kwargs):
        self.server_name = server_name
        self.server_params = server_params

    @asynccontextmanager
    async def session(
        self, 
        *,
        auto_initialize: bool = True
    ) -> AsyncIterator[ClientSession]:
        async with (
            stdio_client(self.server_params) as (read, write),
            ClientSession(read, write) as session,
        ):
            if auto_initialize:
                await session.initialize()
            yield session

