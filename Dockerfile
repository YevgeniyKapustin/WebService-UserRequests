FROM python:3.12.8

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install 'poetry==1.6.1'
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false &&  \
    poetry install --no-interaction --no-ansi --no-dev

COPY . .

CMD chmod a+x /app/scripts/*sh &&  \
    /app/scripts/run_migrations.sh &&  \
    /app/scripts/run_gunicorn.sh
