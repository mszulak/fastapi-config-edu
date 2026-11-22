from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.task import Task
from app.api.tasks import router as tasks_router
from app.core.config import settings


app = FastAPI()
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tasks_router)
@app.get("/")
def read_main():
    return {"service": "ai-backend", "status": "online"}

