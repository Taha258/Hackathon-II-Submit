#backend\api\routes\tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from jose import JWTError, jwt
from typing import Annotated
import os
from datetime import datetime

from core.db import engine
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key")
ALGORITHM = "HS256"

# Database session dependency
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Verify JWT token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return {"user_id": user_id, "email": payload.get("email")}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

TokenDep = Annotated[dict, Depends(verify_token)]

# ----------------- ROUTES -----------------

@router.get("/{user_id}/tasks", response_model=list[TaskResponse])
def list_tasks(user_id: str, session: SessionDep, token_data: TokenDep):
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(user_id: str, task: TaskCreate, session: SessionDep, token_data: TokenDep):
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    db_task = Task(
        title=task.title,
        description=task.description,
        user_id=user_id,
        completed=task.status == "completed",
        status=task.status or "todo",
        priority=task.priority or "medium",
        due_date=task.due_date
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(user_id: str, task_id: int, session: SessionDep, token_data: TokenDep):
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    session: SessionDep,
    token_data: TokenDep
):
    """Update a task with status as master"""
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    # Get task
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    print(f"🔵 Before update - Task {task_id}:")
    print(f"   status={task.status}, completed={task.completed}")
    
    # Get update data
    update_data = task_update.model_dump(exclude_unset=True)
    print(f"🔵 Update data received: {update_data}")
    
    # Update fields
    if "title" in update_data:
        task.title = update_data["title"]
    if "description" in update_data:
        task.description = update_data["description"]
    if "status" in update_data:
        task.status = update_data["status"]
        task.completed = update_data["status"] == "completed"
        print(f"🟢 Setting status={task.status}, completed={task.completed}")
    if "priority" in update_data:
        task.priority = update_data["priority"]
    if "due_date" in update_data:
        task.due_date = update_data["due_date"]

    task.updated_at = datetime.utcnow()
    
    # Save to database
    session.add(task)
    session.commit()
    
    # 🔥 CRITICAL FIX: Detach from session and query fresh
    session.expunge(task)  # Detach from session
    
    # Get completely fresh instance from database
    fresh_task = session.get(Task, task_id)
    
    print(f"🟢 After commit - Fresh from DB:")
    print(f"   status={fresh_task.status}, completed={fresh_task.completed}")
    
    # 🔥 FORCE: Return the fresh instance
    return fresh_task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(user_id: str, task_id: int, session: SessionDep, token_data: TokenDep):
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_complete(user_id: str, task_id: int, session: SessionDep, token_data: TokenDep):
    """Toggle task completion status based on status"""
    if token_data["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    # Toggle between "completed" and "todo"
    task.status = "completed" if task.status != "completed" else "todo"
    task.completed = task.status == "completed"
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task