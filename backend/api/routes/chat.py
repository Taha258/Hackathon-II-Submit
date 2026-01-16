#backend\api\routes\chat.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
import os

try:
    from ai_agent_mcp import chat_with_agent_mcp, MCP_AVAILABLE
    USE_MCP = MCP_AVAILABLE
except ImportError:
    USE_MCP = False

router = APIRouter()
security = HTTPBearer()
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key")
ALGORITHM = "HS256"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    mode: str = "simple"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401,"Invalid token")
        return {"user_id": user_id, "token": credentials.credentials}
    except JWTError:
        raise HTTPException(401,"Invalid token")

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, token_data: dict = Depends(verify_token)):
    user_id = token_data["user_id"]
    auth_token = token_data["token"]

    if USE_MCP:
        response = await chat_with_agent_mcp(request.message, user_id, auth_token)
        mode = "mcp"
    else:
        # Fallback: simple direct AI agent logic
        from ai_agent import chat_with_agent, get_tasks_func, create_task_func, update_task_func, delete_task_func
        task_functions = {"get_tasks": get_tasks_func,"create_task": create_task_func,
                          "update_task": update_task_func,"delete_task": delete_task_func}
        response = await chat_with_agent(request.message, user_id, task_functions)
        mode = "simple"

    return ChatResponse(response=response, mode=mode)
