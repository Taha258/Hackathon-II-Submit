#backend\schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ==================== Task Schemas ====================

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"  # ✅ NEW
    priority: Optional[str] = "medium"  # ✅ NEW
    due_date: Optional[datetime] = None  # ✅ NEW

class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    status: Optional[str] = None  # ✅ NEW
    priority: Optional[str] = None  # ✅ NEW
    due_date: Optional[datetime] = None  # ✅ NEW

class TaskResponse(BaseModel):
    """Schema for task response"""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    status: str  # ✅ NEW
    priority: str  # ✅ NEW
    due_date: Optional[datetime]  # ✅ NEW
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Auth Schemas ====================

class UserCreate(BaseModel):
    """Schema for user registration"""
    name: str
    email: str  # Simple string validation
    password: str

class UserLogin(BaseModel):
    """Schema for user login"""
    email: str  # Simple string validation
    password: str

class UserResponse(BaseModel):
    """Schema for user response"""
    id: str
    email: str
    name: Optional[str] = None
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str
    user: UserResponse