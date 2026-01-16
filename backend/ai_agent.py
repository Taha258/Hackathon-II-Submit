#backend\ai_agent.py
"""
AI Agent for Todo Management
Uses OpenAI Agents SDK with MCP Server
"""
import os
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

load_dotenv()

# MCP Server Configuration
server_params = {
    "command": "python",  # Or "uv" if you're using uv
    "args": ["mcp_server.py"],  # We'll create this next
    "env": os.environ.copy()
}

mcp_server = MCPServerStdio(server_params, client_session_timeout_seconds=60)

def create_todo_agent():
    """Create the Todo AI Agent with MCP tools"""
    return Agent(
        name="TodoAssistant",
        instructions="""
You are a helpful productivity assistant that helps users manage their tasks.

You have access to these tools via MCP:
- get_tasks: List all tasks for a user
- create_task: Create a new task
- update_task: Update existing task (title, description, status, priority, due_date)
- delete_task: Delete a task
- complete_task: Mark a task as completed

Guidelines:
1. Always use the user_id provided in the context (it will be injected automatically)
2. When creating tasks, extract relevant details from user's natural language
3. Be conversational and friendly
4. Confirm actions after completing them
5. If user says "tomorrow", calculate the date
6. For status updates, map natural language to: todo, in-progress, or completed

Examples:
- "Add task to buy groceries" → create_task(title="Buy groceries")
- "Mark task 5 as done" → update_task(task_id=5, status="completed")
- "Show my tasks" → get_tasks()
- "Delete the meeting task" → First get_tasks(), find matching task, then delete_task()

Always respond in a helpful, natural way and confirm what you did.
        """,
        mcp_servers=[mcp_server],
        model="gpt-4o-mini"  # Fast and cost-effective
    )

async def chat_with_agent(message: str, user_id: str) -> str:
    """
    Send a message to the agent and get response
    
    Args:
        message: User's natural language message
        user_id: Authenticated user's ID
        
    Returns:
        Agent's response text
    """
    agent = create_todo_agent()
    
    # Inject user_id into the message context
    enhanced_message = f"[USER_ID: {user_id}] {message}"
    
    async with mcp_server:
        result = await Runner.run(agent, enhanced_message)
        return result.final_output