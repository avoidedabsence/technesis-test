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
  
RUN apt-get -y update; apt-get -y install pip build-essential

RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libnssutil3 libsmime3 libcups2 libxss1 \
    libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxrandr2 \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libgbm1 \
    libgdk-pixbuf2.0-0 libxshmfence1 libpangocairo-1.0-0 \
    libpango-1.0-0 libcairo2 fonts-liberation libdrm2 \
    libxcb-dri3-0 libxinerama1 wget curl unzip ca-certificates \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /src
COPY . ./

RUN chmod -R 777 /src/${DB_PATH}
RUN poetry install
CMD bash -c "cd src && poetry run python start.py"