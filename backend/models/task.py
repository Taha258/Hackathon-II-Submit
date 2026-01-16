#backend\models\task.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)

    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)

    # Status & priority
    status: str = Field(default="todo")        # todo | in-progress | completed
    priority: str = Field(default="medium")    # low | medium | high
    due_date: Optional[datetime] = None

    # 🔑 Foreign Key → user.id
    user_id: Optional[str] = Field(
        default=None,
        foreign_key="user.id",
        index=True
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # ✅ auto-update on UPDATE
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )
