FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false

ENV POETRY_HOME=/opt/poetry
ENV PATH=$POETRY_HOME/bin:$PATH

RUN apk update && apk add --no-cache \
    bash \
    curl \
    nano \
    tree \
    libcap \
    bind-tools \
    nftables \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers \
    openrc \
    docker \
    acl \
    strace \
    findmnt \
    build-base

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s "$POETRY_HOME/bin/poetry" /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

ENV PYTHONPATH="/app"

# RUN mkdir -p /app/tmp

COPY ./scripts /app/scripts
RUN chmod +x /app/scripts/*.sh

EXPOSE 8000

ENTRYPOINT ["/app/scripts/runserver.sh"]
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
