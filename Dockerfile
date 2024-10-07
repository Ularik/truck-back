FROM python:3.11.5-slim-bullseye

# Установка клиента Oracle, раскоментировать если нужно
#RUN set -eux; \
#	pip install --upgrade pip; \
#	savedAptMark="$(apt-mark showmanual)"; \
#	apt-get update; \
#	apt-get install -y --no-install-recommends \
#		dpkg-dev \
#		gcc \
#		gnupg dirmngr \
#		libbluetooth-dev \
#		libbz2-dev \
#		libc6-dev \
#		libexpat1-dev \
#		libffi-dev \
#		libgdbm-dev \
#		liblzma-dev \
#		libncursesw5-dev \
#		libreadline-dev \
#		libsqlite3-dev \
#		libssl-dev \
#		make \
#		tk-dev \
#		uuid-dev \
#		xz-utils \
#		zlib1g-dev; \
#	pip install --no-cache-dir cx_Oracle; \
#	apt-mark auto '.*' > /dev/null; \
#	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; \
#	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
#	rm -rf /var/lib/apt/lists/*;
## Installing Oracle instant client
#WORKDIR    /opt/oracle
#RUN        apt-get update && apt-get install -y libaio1 wget unzip \
#            && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
#            && unzip instantclient-basiclite-linuxx64.zip \
#            && rm -f instantclient-basiclite-linuxx64.zip \
#            && cd /opt/oracle/instantclient* \
#            && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci \
#            && echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
#            && ldconfig

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
RUN apt update -y
RUN apt-get install -y --no-install-recommends mc
RUN apt-get install -y --no-install-recommends build-essential

RUN mkdir -p /usr/www/logs
RUN mkdir -p /usr/www/media
#RUN mkdir -p /usr/www/.venv

RUN python -m pip install --upgrade pip
#RUN pip install pipenv

WORKDIR /usr/www/

COPY requirements.txt .
#COPY Pipfile .
RUN pip install -r requirements.txt

#RUN pipenv install

WORKDIR /usr/www/app/
COPY app .

# CMD ["python", "-m", "daphne", "-b", "0.0.0.0", "-p", "8000", "project.asgi:application"]