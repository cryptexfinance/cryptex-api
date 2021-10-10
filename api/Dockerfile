FROM python:3.8.12-alpine3.14 AS builder
WORKDIR /app
ADD ../requirements.txt /app
RUN apk add gcc musl-dev
RUN pip install -r requirements.txt

FROM python:3.8.12-alpine3.14
WORKDIR /app
ADD .. /app
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
CMD ["python3", "-m", "gunicorn", "-b", "0.0.0.0", "--workers=2", "api:create_app()"]