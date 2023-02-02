FROM python:3.8-slim-bullseye

RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uwsgi

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY nginx-conf/nginx-app.conf /etc/nginx/sites-available/default

COPY nginx-conf/supervisor-app.conf /etc/supervisor/conf.d/

ENV INSTALL_PATH /usr/src/cryptex-api
WORKDIR $INSTALL_PATH

COPY . .

ENV DJANGO_SETTINGS_MODULE cryptex-api.conf.prod
ENV STATIC_ROOT /usr/src/cryptex-api/static/
ENV MEDIA_ROOT /usr/src/cryptex-api/media/

RUN mkdir /usr/src/cryptex-api/media/
RUN chown -R www-data:www-data /usr/src/cryptex-api/media/

EXPOSE 80 443

RUN chmod +x entrypoint.sh
ENTRYPOINT $INSTALL_PATH'/entrypoint.sh'