FROM python:3.8.12-alpine3.14 AS builder
WORKDIR /api
ADD requirements.txt /api
RUN apk add gcc musl-dev
RUN pip install -r requirements.txt
RUN apk update && apk add bash

FROM python:3.8.12-alpine3.14
WORKDIR /api
ADD . /api
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages