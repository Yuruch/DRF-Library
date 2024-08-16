ARG PYTHON_VERSION=3.10.14
FROM python:3.10.14-alpine3.20 as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

chown appuser venv

USER appuser

COPY . .