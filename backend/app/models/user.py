from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.task import Task


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: str | None = None


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    tasks: list[Task] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int
