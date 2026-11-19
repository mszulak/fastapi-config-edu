from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from app.core.config import settings
from app.db.session import get_session
from app.core.celery_app import run_heavy_task
from app.models.task import TaskCreate, Task, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def verify_token(token: str = ""):
    if token != settings.secret_token:
        raise HTTPException(status_code=401)
    return token

@router.post("/", status_code=201, response_model=TaskRead)
def create_task(task: TaskCreate, token: str = Depends(verify_token), session: Session = Depends(get_session)):
    if task.estimated_hours <= 0:
        raise HTTPException(status_code=400, detail="Estimated hours has to be grater than 0")
    if task.estimated_hours > settings.max_hours_limit:
        raise HTTPException(status_code=400, detail=f"Estimated hours has to be less than or equal to {settings.max_hours_limit}")
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    run_heavy_task.delay(db_task.id)
    return db_task

@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} does not exist")
    return task

@router.get("/", response_model=list[TaskRead])
def read_tasks(status: str | None = None, session: Session = Depends(get_session)):
    statement = select(Task)
    if status is not None:
        statement = statement.where(Task.status == status)
    tasks = session.exec(statement).all()
    return tasks

@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_in: TaskUpdate, token: str = Depends(verify_token), session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} does not exist")

    task_data = task_in.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, token: str = Depends(verify_token), session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} does not exist")

    session.delete(db_task)
    session.commit()
    return
