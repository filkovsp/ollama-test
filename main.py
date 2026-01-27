import json
import asyncio
import traceback
from mcp_use import MCPClient
from mcp_use.client.session import MCPSession
from langchain_ollama import ChatOllama
from mcp_use.agents.adapters import LangChainAdapter
from langchain_core.tools import BaseTool

from langchain.agents import create_agent
from langchain.messages import HumanMessage, ToolCall
from mcp.types import Tool

from dotenv import load_dotenv, find_dotenv
load_dotenv()  # Loads from .env file

async def main() -> None:
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
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:/temp"]
    }
    
    filesystem_client = MCPClient()
    filesystem_client.add_server(name = "filesystem", server_config = filesystem_config)
    
    try:
        
        filesystem_session: MCPSession = await filesystem_client.create_session(server_name = "filesystem")
        
        # there is an internal bug in MCPSession, 
        # before calling session.list_tools() we MUST add some timeout 
        # to allow seesion initialize and connect to MCP Server
        await asyncio.sleep(0.25) 
        
        # https://mcp-use.com/docs/python/agent/building-custom-agents
        adapter = LangChainAdapter()
        
        # suggested in mcp-use documentation approach above doesn't really work
        # a workaround is as below:
        filesystem_mcp_tools: list[Tool] = await filesystem_session.list_tools()
        filesystem_tools: list[BaseTool] = [adapter._convert_tool(mcp_tool=tool, connector=filesystem_session.connector) for tool in filesystem_mcp_tools]
        
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
        
        prompt = """
            Using tools available to you perform the following task:
            1. navigate to the repository at D:/temp
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