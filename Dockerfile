FROM python:slim

ARG YOUR_ENV
ARG DB_PATH

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=2.1.2
ENV DB_PATH=${DB_PATH}
  
RUN apt-get -y update; apt-get -y install pip
RUN pip install poetry

WORKDIR /src
COPY . ./

RUN chmod -R 777 /src/${DB_PATH}
RUN poetry install
CMD bash -c "cd src && poetry run python start.py"