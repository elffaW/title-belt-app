# FROM python:3.10-slim
FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    APP_PATH="/opt/app" \
    VENV_PATH="/opt/app/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential
RUN apk add curl

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR $APP_PATH
COPY ./app ./app
COPY ./static ./static
COPY ./web ./web
COPY poetry.lock ./poetry.lock
COPY pyproject.toml ./pyproject.toml

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --only main --no-root

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
