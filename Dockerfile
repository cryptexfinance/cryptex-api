FROM python:3.8.12-alpine3.14
WORKDIR /app
ADD . /app
RUN apk add gcc musl-dev
RUN pip install -r requirements.txt
CMD ["python3", "-m", "gunicorn", "-b", "0.0.0.0", "--workers=2", "api:create_app()"]