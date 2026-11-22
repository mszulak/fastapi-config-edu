from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class TaskBase(SQLModel):
    title: str
    estimated_hours: int
    is_urgent: bool = False
    description: str | None = None


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str = "pending"
    internal_worker_note: str = "secret_log"

    user_id: int | None = Field(default=None, foreign_key="users.id")
    owner: Optional["User"] = Relationship(back_populates="tasks") # noqa: UP037, UP045


class TaskCreate(TaskBase):
    user_id: int | None = None


class TaskRead(TaskBase):
    id: int
    status: str
    user_id: int | None = None


class TaskUpdate(SQLModel):
    title: str | None = None
    estimated_hours: int | None = None
    is_urgent: bool | None = None
    description: str | None = None
