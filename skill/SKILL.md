---
name: mcp-builder
description: Use when the user says "build mcp", "mcp builder", "generate mcp server", or "create mcp for [service]". Guides the user through generating a complete, runnable Python MCP server for any REST API.
---

# Skill: MCP Builder

## What This Skill Does

Generates a complete, working Python MCP server for any REST API. The user provides their API details — you produce a ready-to-run server they can plug into Claude Code immediately.

---

## STEP 1 — Service Name

Ask:
> "What service do you want to connect? (e.g. GoHighLevel, HubSpot, Notion, custom API)"

Wait for the answer. Store as `{SERVICE_NAME}`. Slugify it for file names (lowercase, hyphens): `{service-slug}`.

---

## STEP 2 — Base URL

Ask:
> "What is the base URL of the API? (e.g. https://services.leadconnectorhq.com)"

Wait for the answer. Store as `{BASE_URL}`. Strip trailing slash.

---

## STEP 3 — Authentication

Ask:
> "How does this API authenticate? Options:
> 1. Bearer token — `Authorization: Bearer {key}`
> 2. API key in header — e.g. `X-API-Key: {key}`
> 3. Basic auth — `Authorization: Basic base64(user:pass)`
>
> Which one, and what should the environment variable be called? (e.g. `GHL_API_KEY`)"

Wait for the answer. Store auth method as `{AUTH_METHOD}` and env var name as `{ENV_VAR}`.

---

## STEP 4 — Endpoints

Ask:
> "List the endpoints you want the MCP server to expose. For each one, give me:
> - Method (GET / POST / PUT / DELETE)
> - Path (e.g. /contacts/)
> - What it does in plain English
>
> List 2–5 endpoints. Paste them all at once."

Wait for the answer. Parse into a list of `{ENDPOINTS}`.

---

## STEP 5 — Generate the MCP Server

Create the file `projects/mcp-{service-slug}/server.py`.

Use this structure exactly. Fill in all placeholders from what the user provided:

```python
import asyncio
import os
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

{ENV_VAR} = os.environ.get("{ENV_VAR}", "")
BASE_URL = "{BASE_URL}"

server = Server("{service-slug}-mcp")


def get_headers() -> dict:
    # BUILD AUTH HEADER BASED ON AUTH_METHOD
    # Bearer token:
    return {"Authorization": f"Bearer { {ENV_VAR} }"}
    # API key header (replace header name as needed):
    # return {"X-API-Key": {ENV_VAR}}


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ONE TOOL PER ENDPOINT — fill from {ENDPOINTS}
        Tool(
            name="tool_name",
            description="Plain English description",
            inputSchema={
                "type": "object",
                "properties": {
                    # Add relevant parameters here
                    "limit": {"type": "integer", "description": "Max results", "default": 20}
                },
                "required": []
            }
        ),
        # ... repeat for each endpoint
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    headers = get_headers()
    async with httpx.AsyncClient() as client:
        # ROUTE BY TOOL NAME — one block per endpoint
        if name == "tool_name":
            resp = await client.get(f"{BASE_URL}/path/", headers=headers, params=arguments)
            resp.raise_for_status()
            return [TextContent(type="text", text=resp.text)]

        raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
```

Generate the actual file with real tool names, real paths, and real parameters derived from the endpoints the user listed. Do not leave placeholders — write the full working code.

---

## STEP 6 — Generate requirements.txt

Create `projects/mcp-{service-slug}/requirements.txt`:

```
mcp
httpx
```

---

## STEP 7 — Show Config Snippet

Tell the user:

> "Add this to your `.claude/settings.json` under `mcpServers`:"

```json
"{service-slug}": {
  "command": "python",
  "args": ["projects/mcp-{service-slug}/server.py"],
  "env": {
    "{ENV_VAR}": "your-api-key-here"
  }
}
```

---

## STEP 8 — Show Test Instructions

Tell the user:

> "To test it:
> 1. `pip install mcp httpx`
> 2. Add the config snippet above to `.claude/settings.json`
> 3. Restart Claude Code
> 4. Ask me to use one of the tools — e.g. 'use the {service-slug} MCP to [do something]'
> 5. If it works, you'll see the tool call and response in the conversation."

---

## STEP 9 — Optional GitHub Push

Ask:
> "Want to push this to GitHub as a portfolio piece?"

If yes: invoke the `github-publish` skill with the `projects/mcp-{service-slug}/` folder.

If no: done.

---

## Rules

- Generate real, complete code — no `...` or placeholder comments left in the output
- Never hardcode API keys — always use environment variables
- Keep tool names snake_case and descriptive (e.g. `get_contacts`, `create_lead`)
- If the user gives vague endpoints, ask one follow-up question before generating
- The generated server must be runnable with `python server.py` after `pip install mcp httpx`
