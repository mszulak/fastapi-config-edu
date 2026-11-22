from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    title: str
    estimated_hours: int
    is_urgent: bool = False
    description: str | None = None


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str = "pending"
    internal_worker_note: str = "secret_log"


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    status: str


class TaskUpdate(SQLModel):
    title: str | None = None
    estimated_hours: int | None = None
    is_urgent: bool | None = None
    description: str | None = None
