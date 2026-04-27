# MCP Server Builder

> A Claude Code skill that generates production-ready MCP (Model Context Protocol) servers for any REST API — so you can talk to any tool, CRM, or service in plain English through Claude.


## What This Does

## How It Works
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
|---|---|
| GoHighLevel | get contacts, create leads, update pipeline |
| HubSpot | search deals, create contacts, log activity |
| Notion | read/write pages and databases |
| Airtable | query and update records |
| Slack | send messages, read channels |
| Any custom API | whatever endpoints you need |

## Using the Skill
2. Open Claude Code and say **"build mcp"**
3. Answer the 4 questions
4. Follow the generated setup instructions

## Example: GoHighLevel MCP Server
- `get_contact` — fetch a single contact by ID
- `create_contact` — create a new CRM contact
- `update_contact` — update an existing contact
- `get_opportunities` — list pipeline deals
```bash
cd examples/ghl
pip install -r requirements.txt
cp .env.example .env
# Add your GHL Private Integration Token to .env
```
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
> "Show me all contacts named Nikos in GHL"
> "Create a new lead — Maria Papadopoulou, maria@company.gr"
> "What opportunities do I have open in the pipeline?"

## Tech Stack
- **MCP SDK** — Anthropic's Model Context Protocol library
- **httpx** — async HTTP client for API calls
- **python-dotenv** — local environment variable management

## Security
- `.gitignore` blocks `.env` automatically
- `.env.example` ships as a safe placeholder

## Use Cases
- **Agencies running GoHighLevel** — control your CRM through conversation: look up contacts, create leads, and check pipeline status without leaving your terminal
- **Developers** — skip the plumbing and go straight to building; every REST API becomes a natural language interface through Claude Code
Built by [Theo](https://github.com/theokalogr-bit) — AI automation consultant based in Greece.
