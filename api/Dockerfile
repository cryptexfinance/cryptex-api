FROM python:3.8-slim-buster

WORKDIR /usr/src/api

RUN apt-get update && apt-get upgrade
RUN apt-get -y install gcc

ENV FLASK_RUN_HOST=0.0.0.0
#Server will reload itself on file changes if in dev mode
ENV FLASK_ENV=development 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["flask", "run"]