import os
import asyncio
import traceback
from pathlib import Path

from mcp_use import MCPClient
from mcp_use.client.session import MCPSession

from langchain_ollama import ChatOllama
from langchain_core.tools import BaseTool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools

from dotenv import load_dotenv
load_dotenv()  # Loads from .env file

async def main() -> None:
    root_path = str(Path("~/Documents").expanduser().resolve())
    
    # follow documentation and create MCP Server config.
    # https://mcp-use.com/docs/python/client/client-configuration
    # https://mcp-use.com/docs/python/client/direct-tool-calls
    # mcp_config = {
    #     "mcpServers": {
    #         "filesystem": {
    #             "command": "npx",
    #             "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:/temp"]
    #         }
    #     }
    # }
    # 
    # client = MCPClient(config = mcp_config)
    
    # in case of multiple agents with different list of tools allowed to be used
    # we need to create multiple clients with different configs
    filesystem_config = {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", root_path],
        "cwd": os.getcwd(),
    }
    
    filesystem_client = MCPClient()
    filesystem_client.add_server(name = "filesystem", server_config = filesystem_config)
    
    try:
        
        filesystem_session: MCPSession = await filesystem_client.create_session(server_name = "filesystem")
        
        # there is an internal bug in MCPSession, 
        # before calling session.list_tools() we MUST add some timeout 
        # to allow seesion initialize and connect to MCP Server
        await asyncio.sleep(0.25)
        
        # suggested in mcp-use documentation approach above doesn't really work
        # a workaround is load_mcp_tools which comes with https://reference.langchain.com/python/langchain_mcp_adapters
        await filesystem_session.list_tools() # need to make this call, otherwise the below is failing...
        filesystem_tools: list[BaseTool] = await load_mcp_tools(filesystem_session.connector.client_session)
        
        # https://docs.langchain.com/oss/python/langchain/models
        ollama_model = ChatOllama(
            model="gpt-oss:20b",
            validate_model_on_init=True,
            temperature=0,
            base_url="http://localhost:11434",
        )
        
        # https://docs.langchain.com/oss/python/langchain/agents
        agent = create_agent(
            name="filesystem_agent",
            model=ollama_model, 
            tools=filesystem_tools, 
            system_prompt="You are a developer with access to Filesystem MCP tools",
            
            # see also:
            # https://docs.langchain.com/oss/python/langchain/agents#structured-output
            # https://docs.langchain.com/oss/python/langchain/structured-output
        )
        
        prompt = f"""
            Using tools available to you perform the following task:
            1. navigate to the directory at {root_path}
            2. find existing file in it named `hello.txt` with the content 'Hello!'
            3. Modify the content of `hello.txt` to 'Hello, World!'
            if the file does not exist, create it with the content 'Hello, World!'
        """
        
        # async invokation:
        # https://docs.langchain.com/oss/python/langchain/agents#invocation
        result = await agent.ainvoke(input={"messages": [HumanMessage(prompt)]})
        print(result["messages"][-1].text)
        
        
        # see also streaming:
        # https://docs.langchain.com/oss/python/langchain/streaming/overview
        # but remember to use astream() - async stream.
        # async for token, metadata in agent.astream(  
        #     input={"messages": [HumanMessage(prompt)]},
        #     stream_mode="messages",
        # ):
        #     print(json.dumps(obj={
        #         "node": f"{metadata['langgraph_node']}",
        #         "content": f"{token.content_blocks}",
        #     }, default=str, indent=2))
        
    except Exception as e:
        print("oops....")
        traceback.print_exc()

    finally:
        await filesystem_client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())