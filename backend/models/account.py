#backend\models\account.py
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


def generate_uuid() -> str:
    """Generate a new UUID string"""
    return str(uuid.uuid4())


class Account(SQLModel, table=True):
    """Account model for authentication providers"""
    
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        nullable=False
    )
    account_id: str = Field(sa_column_kwargs={"name": "accountId"})
    provider_id: str = Field(sa_column_kwargs={"name": "providerId"})
    user_id: str = Field(sa_column_kwargs={"name": "userId"})
    access_token: Optional[str] = Field(default=None, sa_column_kwargs={"name": "accessToken"})
    refresh_token: Optional[str] = Field(default=None, sa_column_kwargs={"name": "refreshToken"})
    id_token: Optional[str] = Field(default=None, sa_column_kwargs={"name": "idToken"})
    expires_at: Optional[int] = Field(default=None, sa_column_kwargs={"name": "expiresAt"})
    password: Optional[str] = None