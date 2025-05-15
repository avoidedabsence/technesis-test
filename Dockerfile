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

RUN sudo apt-get -y install \
libatk-bridge2.0-0 \
libatk1.0-0 \
libcups2 \
libglib2.0-0 \
libgtk-3-0 \
libnss3 \
libxss1 \
xdg-utils \
ca-certificates \
fonts-liberation \
libnspr4 \
lsb-release \
wget \
libayatana-appindicator3-1 \
libayatana-appindicator3-dev \
gir1.2-ayatanaappindicator3-0.1

RUN sudo apt-get -y install \
gconf-service \
libasound2 \
libappindicator1 \
libgconf-2-4

RUN pip install poetry

WORKDIR /src
COPY . ./

RUN chmod -R 777 /src/${DB_PATH}
RUN poetry install
CMD bash -c "cd src && poetry run python start.py"