# MCP Server Builder

> A Claude Code skill that generates production-ready MCP (Model Context Protocol) servers for any REST API — so you can talk to any tool, CRM, or service in plain English through Claude.

## What This Does

Most developers interact with APIs by writing code — HTTP requests, parsing JSON, handling errors. This skill removes that entirely. You provide an API name, base URL, API key, and a list of endpoints. Claude generates a complete, runnable MCP server that connects that API directly to Claude Code.

Once connected, you control the API through natural language. No code. No clicking. Just conversation.

Built on Anthropic's [Model Context Protocol](https://modelcontextprotocol.io/) — the open standard for connecting AI assistants to external tools.

## How It Works

```
You say: "build mcp"
         │
         ▼
Claude asks 4 questions:
  1. What service? (e.g. HubSpot, Notion, GoHighLevel)
  2. What's the base URL?
  3. How does it authenticate? (Bearer / API key / Basic)
  4. Which endpoints do you want?
         │
         ▼
Claude generates:
  - server.py       ← complete, runnable MCP server
  - requirements.txt
  - .env.example    ← safe placeholder for your API key
  - config snippet  ← paste into Claude Code settings
         │
         ▼
You restart Claude Code.
Now you control that API through conversation.
```

## What You Can Build

Any service with a REST API works:

| Service | Example Tools |
|---|---|
| GoHighLevel | get contacts, create leads, update pipeline |
| HubSpot | search deals, create contacts, log activity |
| Notion | read/write pages and databases |
| Airtable | query and update records |
| Slack | send messages, read channels |
| Any custom API | whatever endpoints you need |

## Using the Skill

This skill runs inside [Claude Code](https://claude.ai/code). To use it:

1. Copy `skill/SKILL.md` into your `.claude/skills/mcp-builder/` folder
2. Open Claude Code and say **"build mcp"**
3. Answer the 4 questions
4. Follow the generated setup instructions

## Example: GoHighLevel MCP Server

A working example is included in `examples/ghl/`. It exposes 5 tools:

- `get_contacts` — search contacts by name, email, or phone
- `get_contact` — fetch a single contact by ID
- `create_contact` — create a new CRM contact
- `update_contact` — update an existing contact
- `get_opportunities` — list pipeline deals

**Setup:**
```bash
cd examples/ghl
pip install -r requirements.txt
cp .env.example .env
# Add your GHL Private Integration Token to .env
```

Add to Claude Code `settings.json`:
```json
{
  "mcpServers": {
    "ghl": {
      "command": "python",
      "args": ["examples/ghl/server.py"],
      "env": {}
    }
  }
}
```

Then ask Claude:
> "Show me all contacts named Nikos in GHL"
> "Create a new lead — Maria Papadopoulou, maria@company.gr"
> "What opportunities do I have open in the pipeline?"

## Tech Stack

- **Python** — MCP server runtime
- **MCP SDK** — Anthropic's Model Context Protocol library
- **httpx** — async HTTP client for API calls
- **python-dotenv** — local environment variable management

## Security

- API keys are stored in `.env` only — never committed to git
- `.gitignore` blocks `.env` automatically
- `.env.example` ships as a safe placeholder

---
Built by [Theo](https://github.com/theokalogr-bit) — AI automation consultant based in Greece.
