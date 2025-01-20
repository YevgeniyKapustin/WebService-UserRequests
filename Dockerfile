FROM python:3.12.8

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG DEV=false
ENV DEV=${DEV}

RUN pip install 'poetry==1.6.1'
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi \
    $(["$DEV" = "true"] && echo "--without dev" || echo "")

COPY . .
