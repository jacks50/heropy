FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt-get update
RUN apt-get -y --no-install-recommends install curl
RUN curl -sSL https://install.python-poetry.org | python

ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false
RUN poetry install

COPY manage.py ./

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
