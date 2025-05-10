FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip wheel "poetry==2.1.3"

WORKDIR /app

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/

RUN poetry install

COPY . /app

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "src/main.py"]
