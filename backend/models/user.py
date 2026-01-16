#backend\models\user.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


def generate_uuid() -> str:
    """Generate a new UUID string"""
    return str(uuid.uuid4())


class User(SQLModel, table=True):
    """User model for authentication"""
    
    __tablename__ = "user"  # ✅ CRITICAL
    
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        nullable=False
    )
    name: str
    email: str = Field(unique=True, index=True)
    email_verified: bool = Field(default=False, sa_column_kwargs={"name": "emailVerified"})
    image: Optional[str] = None
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"name": "createdAt"}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"name": "updatedAt", "onupdate": datetime.utcnow}
    )