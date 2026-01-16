# backend/mcp_server.py
import asyncio
import os
import httpx
from typing import Dict, Any, List

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️ MCP not installed. Run: uv add 'mcp[cli]'")

if not MCP_AVAILABLE:
    exit(1)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # Must match FastAPI

app = Server("todo-task-manager")

@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="get_tasks",
            description="Get all tasks for a user",
            inputSchema={"type": "object","properties":{"user_id":{"type":"string"}},"required":["user_id"]}
        ),
        Tool(
            name="create_task",
            description="Create a new task",
            inputSchema={
                "type":"object",
                "properties":{"user_id":{"type":"string"},"title":{"type":"string"},"description":{"type":"string"},"status":{"type":"string"},"priority":{"type":"string"},"due_date":{"type":"string"}},
                "required":["user_id","title"]
            }
        ),
        Tool(
            name="update_task",
            description="Update an existing task",
            inputSchema={
                "type":"object",
                "properties":{"user_id":{"type":"string"},"task_id":{"type":"integer"},"title":{"type":"string"},"description":{"type":"string"},"status":{"type":"string"},"priority":{"type":"string"},"due_date":{"type":"string"}},
                "required":["user_id","task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={"type":"object","properties":{"user_id":{"type":"string"},"task_id":{"type":"integer"}},"required":["user_id","task_id"]}
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    user_id = arguments.get("user_id") or os.getenv("USER_ID")
    headers = {}
    token = os.getenv("USER_AUTH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        try:
            if name == "get_tasks":
                resp = await client.get(f"{BACKEND_URL}/api/{user_id}/tasks", headers=headers)
                resp.raise_for_status()
                tasks = resp.json()
                return [TextContent(type="text", text=str(tasks))]

            elif name == "create_task":
                payload = {k: arguments.get(k) for k in ["title","description","status","priority","due_date"] if arguments.get(k) is not None}
                resp = await client.post(f"{BACKEND_URL}/api/{user_id}/tasks", json=payload, headers=headers)
                resp.raise_for_status()
                task = resp.json()
                return [TextContent(type="text", text=str(task))]

            elif name == "update_task":
                task_id = arguments.get("task_id")
                payload = {k: arguments.get(k) for k in ["title","description","status","priority","due_date"] if arguments.get(k) is not None}
                resp = await client.put(f"{BACKEND_URL}/api/{user_id}/tasks/{task_id}", json=payload, headers=headers)
                resp.raise_for_status()
                task = resp.json()
                return [TextContent(type="text", text=str(task))]

            elif name == "delete_task":
                task_id = arguments.get("task_id")
                resp = await client.delete(f"{BACKEND_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
                resp.raise_for_status()
                return [TextContent(type="text", text="Task deleted successfully")]

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
        
        except httpx.HTTPStatusError as e:
            return [TextContent(type="text", text=f"Error: {e.response.status_code} {e.response.reason_phrase} - {e.response.text}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
