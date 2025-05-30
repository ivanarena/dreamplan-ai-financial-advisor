FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/components:/documents:/calculation:/templates:/static:."

RUN pip install uv

COPY pyproject.toml .

RUN uv sync

COPY . .

CMD ["uv", "run", "uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]
