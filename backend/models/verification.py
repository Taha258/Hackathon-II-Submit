from sqlmodel import SQLModel, Field
from datetime import datetime

class Verification(SQLModel, table=True):
    __tablename__ = "verification"
    
    id: str = Field(primary_key=True)
    identifier: str
    value: str
    expiresAt: datetime