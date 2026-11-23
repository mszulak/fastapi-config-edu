from typing import Annotated

from fastapi import Depends, HTTPException

from app.core.config import settings
from app.db.session import SessionDep  # noqa: F401


def verify_token(token: str = ""):
    if token != settings.secret_token:
        raise HTTPException(status_code=401)
    return token


TokenDep = Annotated[str, Depends(verify_token)]
