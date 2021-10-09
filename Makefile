run-debug-server:
	FLASK_APP=api FLASK_ENV=development python3 -m flask run

run-server:
	gunicorn --workers=2 "api:create_app()"

image:
	pipenv lock --keep-outdated --requirements > requirements.txt
	docker build .
	rm requirements.txt