FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip wheel "poetry==2.1.3"

WORKDIR /app

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/

RUN poetry install

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "telegram_bot/main.py"]
