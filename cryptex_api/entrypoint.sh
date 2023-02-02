
#!/bin/bash
apt update && apt upgrade
apt-get -y install apt-utils
apt-get -y install curl
apt-get -y install gnupg2

# Run requirements
echo "Run requirements"
pip install -r requirements.txt

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput -i node_modules

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
gunicorn cryptex_api.wsgi:application --bind 0.0.0.0:8005
