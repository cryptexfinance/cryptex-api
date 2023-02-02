FROM python:3.8-slim-bullseye

RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*
ENV INSTALL_PATH /usr/src/cryptex-api/cryptex_api
WORKDIR $INSTALL_PATH

COPY . .

ENV DJANGO_SETTINGS_MODULE cryptex_api.settings

RUN mkdir /usr/src/cryptex-api/media/
RUN chown -R www-data:www-data /usr/src/cryptex-api/media/

EXPOSE 8005

RUN chmod +x entrypoint.sh
ENTRYPOINT $INSTALL_PATH'/entrypoint.sh'