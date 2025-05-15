FROM python:slim

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=2.1.2

RUN apt-get -y update; apt-get -y install build-essential pip
RUN pip install poetry

WORKDIR /src
COPY . ./

RUN poetry install
CMD bash -c "cd src && poetry run python start.py"