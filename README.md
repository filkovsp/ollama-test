# Get started with local LM Studio as LLM Provider 

## 1. Ollama binaries:
Download and install from https://ollama.com/download

## 2. Download model(s)
- Gemini gemma3: 
```bash
ollama pull gemma3:27b
```
- GPT-OSS:
```bash
ollama pull gpt-oss:20b

# or 
ollama pull gpt-oss:120b
```

## 3. Setup local Python project
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
npm ci

# make sure you've got NodeJS v20+ installed
```
4. run python application:
```bash
uv run --env-file .env -- main.py
```
