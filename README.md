# Get started with local LM Studio as LLM Provider 

## 1. Install LM Studio
Download and install from https://lmstudio.ai/download
When that's done, download and start LLM, for example "meta-llama-3.1-8b-instruct".

## 2. Setup local Python project
1. Install UV from https://docs.astral.sh/uv/getting-started/installation/
2. Restart your Terminals, VS Code IDE, etc.. and run command in console:
```bash
uv sync
```
then
```bash
# for Windows:
source .venv/Scripts/activate

# for OSX:
source .venv/bin/activate
```
then 
```bash
python -m ensurepip
```
3. Install  Filesystem MCP Server
```bash
npm install -g @modelcontextprotocol/server-filesystem
```
4. run python application:
```bash
uv run --env-file .env -- main.py
```
