# Test communication with a MCP server

## Install MCP Server if needed. 
example: Filesystem MCP Server based on Node JS:
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

## Run mcp server as standalone application in stdio mode:
- Git MCP Server:
```bash
python -m mcp_server_git
```
- Filesystem MCP Server:
```bash
npx -y @modelcontextprotocol/server-filesystem /Users/pfilkovskyi/Projects
```

interact with MCP server through terminal
---
1. send handshake:
    __Note__: this handshake and any other JSON RPC commands listed below should be sent into terminal's stdio as a single line text. Minimize the below json in browser's dev console as `JSON.stringify({....})` - when copying the json string ommit wrapping single quotes `'`.
    ```json
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {
                "name": "pavlo-client",
                "version": "0.1.0"
            }
        }
    }
    ```
2. list available tools:
    ```json
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    ```
3. Call Tool.
    For example, `list_directory` tool in filesystem mcp server:
    ```json
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "list_directory",
            "arguments": {
                "path": "/absolute/path/to/the-directory"
            }
        }
    }
    ```