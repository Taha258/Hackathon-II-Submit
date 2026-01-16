#backend\main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from jose import JWTError, jwt
from typing import Annotated
import os
from contextlib import asynccontextmanager

from core.db import engine, create_db_and_tables, get_session
# ✅ IMPORTANT: Import models AFTER db setup
from schemas import TaskCreate, TaskUpdate, TaskResponse

# Import auth and chat routes
from api.routes import auth
from api.routes import chat  # ✅ NEW: Import chat router

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting up application...")
    try:
        # ✅ Import models HERE before creating tables
        from models import User, Task, Account, Session as DBSession, Verification
        
        create_db_and_tables()
        print("✅ Application started successfully")
    except Exception as e:
        print(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
    yield
    # Shutdown
    print("👋 Shutting down application...")
    engine.dispose()  # Close all connections properly
    print("✅ Cleanup completed")

app = FastAPI(
    title="Todo API",
    version="2.0",
    description="Todo API with Authentication",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000","https://hackathon-ii-front-end.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(chat.router)  # ✅ NEW: Include chat router

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key")
ALGORITHM = "HS256"

# Database Session Dependency
SessionDep = Annotated[Session, Depends(get_session)]

# JWT Verification
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token and extract user info"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "email": payload.get("email")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

TokenDep = Annotated[dict, Depends(verify_token)]

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "message": "Todo API is running", 
        "version": "2.0",
        "status": "healthy",
        "endpoints": {
            "docs": "/docs",
            "auth": "/auth",
            "tasks": "/api/{user_id}/tasks",
            "chat": "/chat"  # ✅ NEW: Document chat endpoint
        }
    }

@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "ok",
        "database": "connected"
    }

# Task Endpoints

@app.get("/api/{user_id}/tasks", response_model=list[TaskResponse])
def list_tasks(user_id: str, session: SessionDep, token_data: TokenDep):
    """List all tasks for authenticated user"""
    # ✅ Import here to avoid circular issues
    from models import Task
    
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

@app.post("/api/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(user_id: str, task: TaskCreate, session: SessionDep, token_data: TokenDep):
    """Create a new task"""
    # ✅ Import here
    from models import Task
    
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db_task = Task(
        title=task.title,
        description=task.description,
        user_id=user_id,
        completed=False
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.get("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(user_id: str, task_id: int, session: SessionDep, token_data: TokenDep):
    """Get task details"""
    from models import Task
    
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(user_id: str, task_id: int, task_update: TaskUpdate, session: SessionDep, token_data: TokenDep):
    """Update a task"""
    from models import Task
    
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/api/{user_id}/tasks/{task_id}")
def delete_task(user_id: str, task_id: int, session: SessionDep, token_data: TokenDep):
    """Delete a task"""
    from models import Task
    
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}

@app.patch("/api/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_complete(user_id: str, task_id: int, session: SessionDep, token_data: TokenDep):
    """Toggle task completion status"""
    from models import Task
    
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task