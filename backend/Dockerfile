FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY pyproject.toml uv.lock ./
COPY ./app ./app

COPY alembic.ini ./
COPY ./alembic ./alembic

RUN uv sync --frozen --no-dev
