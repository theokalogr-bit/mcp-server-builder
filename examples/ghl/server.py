import asyncio
import os
from dotenv import load_dotenv
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

load_dotenv()

GHL_API_KEY = os.environ.get("GHL_API_KEY", "")
GHL_LOCATION_ID = os.environ.get("GHL_LOCATION_ID", "")
BASE_URL = "https://services.leadconnectorhq.com"

server = Server("ghl-mcp")


def get_headers() -> dict:
    return {
        "Authorization": f"Bearer {GHL_API_KEY}",
        "Version": "2021-07-28",
        "Content-Type": "application/json",
    }


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_contacts",
            description="Search and list contacts in GoHighLevel",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term (name, email, phone)"},
                    "limit": {"type": "integer", "description": "Max contacts to return", "default": 20},
                },
                "required": [],
            },
        ),
        Tool(
            name="get_contact",
            description="Get a single contact by their ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string", "description": "The GHL contact ID"},
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="create_contact",
            description="Create a new contact in GoHighLevel",
            inputSchema={
                "type": "object",
                "properties": {
                    "first_name": {"type": "string", "description": "Contact's first name"},
                    "last_name": {"type": "string", "description": "Contact's last name"},
                    "email": {"type": "string", "description": "Contact's email address"},
                    "phone": {"type": "string", "description": "Contact's phone number"},
                },
                "required": ["first_name"],
            },
        ),
        Tool(
            name="update_contact",
            description="Update an existing contact's details",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string", "description": "The GHL contact ID"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="get_opportunities",
            description="List opportunities (deals) in the pipeline",
            inputSchema={
                "type": "object",
                "properties": {
                    "pipeline_id": {"type": "string", "description": "Pipeline ID to filter by"},
                    "limit": {"type": "integer", "description": "Max opportunities to return", "default": 20},
                },
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    headers = get_headers()

    async with httpx.AsyncClient(timeout=30.0) as client:

        if name == "get_contacts":
            params = {"locationId": GHL_LOCATION_ID, "limit": arguments.get("limit", 20)}
            if arguments.get("query"):
                params["query"] = arguments["query"]
            resp = await client.get(f"{BASE_URL}/contacts/", headers=headers, params=params)
            resp.raise_for_status()
            return [TextContent(type="text", text=resp.text)]

        if name == "get_contact":
            contact_id = arguments["contact_id"]
            resp = await client.get(f"{BASE_URL}/contacts/{contact_id}", headers=headers)
            resp.raise_for_status()
            return [TextContent(type="text", text=resp.text)]

        if name == "create_contact":
            body = {"locationId": GHL_LOCATION_ID}
            for field in ("first_name", "last_name", "email", "phone"):
                if arguments.get(field):
                    key = "firstName" if field == "first_name" else "lastName" if field == "last_name" else field
                    body[key] = arguments[field]
            resp = await client.post(f"{BASE_URL}/contacts/", headers=headers, json=body)
            resp.raise_for_status()
            return [TextContent(type="text", text=resp.text)]

        if name == "update_contact":
            contact_id = arguments["contact_id"]
            body = {}
            for field in ("first_name", "last_name", "email", "phone"):
                if arguments.get(field):
                    key = "firstName" if field == "first_name" else "lastName" if field == "last_name" else field
                    body[key] = arguments[field]
            resp = await client.put(f"{BASE_URL}/contacts/{contact_id}", headers=headers, json=body)
            resp.raise_for_status()
            return [TextContent(type="text", text=resp.text)]

        if name == "get_opportunities":
            params = {"location_id": GHL_LOCATION_ID, "limit": arguments.get("limit", 20)}
            if arguments.get("pipeline_id"):
                params["pipeline_id"] = arguments["pipeline_id"]
            resp = await client.get(f"{BASE_URL}/opportunities/search", headers=headers, params=params)
            resp.raise_for_status()
            return [TextContent(type="text", text=resp.text)]

        raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
