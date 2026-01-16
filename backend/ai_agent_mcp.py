# backend/ai_agent_mcp.py
import os
import json
from dotenv import load_dotenv

load_dotenv()

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from openai import AsyncOpenAI
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️ MCP packages not installed")

if MCP_AVAILABLE:
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def chat_with_agent_mcp(message: str, user_id: str, auth_token: str) -> str:
        try:
            env = os.environ.copy()
            env["USER_AUTH_TOKEN"] = auth_token
            env["USER_ID"] = user_id

            server_params = StdioServerParameters(
                command="python",
                args=["mcp_server.py"],
                env=env
            )

            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools_result = await session.list_tools()
                    tools = tools_result.tools

                    system_prompt = f"""
You are a helpful assistant managing tasks for user {user_id}.
Use the available tools to create, update, delete, or list tasks.
Be friendly and confirm actions. When a task is created, say "Task created successfully!"
"""

                    # First OpenAI call
                    response = await client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": message}
                        ],
                        tools=[{
                            "type": "function",
                            "function": {
                                "name": t.name,
                                "description": t.description or "",
                                "parameters": t.inputSchema
                            }
                        } for t in tools],
                        tool_choice="auto"
                    )

                    message_obj = response.choices[0].message

                    if not hasattr(message_obj, "tool_calls") or not message_obj.tool_calls:
                        return message_obj.content or "I don't understand."

                    # ✅ Execute tool calls and collect results
                    tool_results = []
                    
                    for tool_call in message_obj.tool_calls:
                        try:
                            tool_result = await session.call_tool(
                                tool_call.function.name,
                                arguments=json.loads(tool_call.function.arguments)
                            )
                            
                            # ✅ Extract text from CallToolResult
                            result_text = ""
                            if tool_result and hasattr(tool_result, 'content'):
                                for content_item in tool_result.content:
                                    if hasattr(content_item, 'text'):
                                        result_text += content_item.text
                            
                            tool_results.append({
                                "tool": tool_call.function.name,
                                "result": result_text or "Success"
                            })
                            
                        except Exception as e:
                            print(f"❌ Tool call error: {e}")
                            tool_results.append({
                                "tool": tool_call.function.name,
                                "result": f"Error: {str(e)}"
                            })

                    # ✅ Second OpenAI call with tool results
                    final_response = await client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": message},
                            {"role": "assistant", "content": f"Tool results: {json.dumps(tool_results)}"}
                        ]
                    )

                    return final_response.choices[0].message.content or "Task completed!"

        except Exception as e:
            print(f"❌ MCP Error: {e}")
            import traceback
            traceback.print_exc()
            return f"Error: {str(e)}"

else:
    async def chat_with_agent_mcp(message: str, user_id: str, auth_token: str) -> str:
        return "MCP Server not available. Please install: uv add 'mcp[cli]' openai"