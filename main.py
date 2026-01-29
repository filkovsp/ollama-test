import asyncio
import traceback
from pathlib import Path

from mcp_client import GitMCPClient, FilesystemMCPClient

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools

from dotenv import load_dotenv
load_dotenv()  # Loads from .env file

async def main() -> None:
    root_path = str(Path("~/Documents").expanduser().resolve())

    filesystem_mcp_client = FilesystemMCPClient(server_name="filesystem", root_path=root_path)
    git_mcp_client = GitMCPClient(server_name="git")

    async with \
            filesystem_mcp_client.session() as filesystem_session, \
            git_mcp_client.session() as git_session:

        await asyncio.sleep(0.25)

        try:
            filesystem_tools = await load_mcp_tools(session=filesystem_session)
            git_tools = await load_mcp_tools(session=git_session)

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
                tools=(filesystem_tools + git_tools),
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

if __name__ == "__main__":
    asyncio.run(main())