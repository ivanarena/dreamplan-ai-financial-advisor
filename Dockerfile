FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y && apt-get clean

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/components:/documents:/calculation:/templates:/static:."

RUN pip install uv

COPY pyproject.toml .

RUN uv sync

COPY . .

CMD ["uv", "run", "gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "8", "--bind", "0.0.0.0:8000"]
