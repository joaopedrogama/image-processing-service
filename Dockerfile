FROM python:3.12.4-slim-bookworm

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR "/usr/src/app/"
STOPSIGNAL SIGINT

RUN mkdir -p \
        "/usr/src/app/" \
        "/var/www/image_processing_service/static/" \
        "/var/www/image_processing_service/media/" \
        "/var/log/image_processing_service/" && \
    apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
        build-essential ca-certificates gettext gnupg1 \
        libffi-dev libpq-dev libssl1.0 libxml2-dev libxmlsec1-dev libxmlsec1-openssl libxslt-dev \
        memcached netcat-traditional postgresql-client python3-dev libmagic1 && \
    pip install --no-input --no-cache-dir --upgrade \
        pip setuptools wheel && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/*

ARG MODE
COPY ["./app/requirements/", "./app/docker/build.sh", "/tmp/main/"]
RUN sh "/tmp/main/build.sh" "/tmp/main" && \
    rm -rf "/tmp/main/"

EXPOSE 8001

COPY ["./app/", "/usr/src/app/"]
ENTRYPOINT ["sh", "/usr/src/app/docker/start.sh"]
