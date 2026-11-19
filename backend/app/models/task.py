from sqlmodel import SQLModel, Field


class TaskCreate(SQLModel):
    title: str
    estimated_hours: int
    is_urgent: bool = False

class Task(TaskCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str = "pending"
    internal_worker_note: str = "secret_log"

class TaskRead(TaskCreate):
    id: int
    status: str

class TaskUpdate(SQLModel):
    title: str | None = None
    estimated_hours: int | None = None
    is_urgent: bool | None = None
