from sqlmodel import SQLModel, Field
from datetime import datetime

class Session(SQLModel, table=True):
    __tablename__ = "session"
    
    id: str = Field(primary_key=True)
    expiresAt: datetime
    ipAddress: str = Field(default="")
    userAgent: str = Field(default="")
    userId: str = Field(foreign_key="user.id", index=True)
    token: str = Field(unique=True, index=True)