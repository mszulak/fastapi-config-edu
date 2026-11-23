from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep, TokenDep
from app.core.config import settings  # noqa: F401
from app.models.user import User, UserCreate, UserRead, UserReadWithTasks

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=201, response_model=UserRead)
def create_user(user: UserCreate, token: TokenDep, session: SessionDep):
    if session.exec(select(User).where(User.email == user.email)).first() is not None:
        raise HTTPException(
            status_code=409, detail="User with this email already exists"
        )
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=UserReadWithTasks)
def read_user_with_tasks(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} does not exist"
        )
    return user
