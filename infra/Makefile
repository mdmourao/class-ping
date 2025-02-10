setup:
	sudo apt update
	sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl


setup_db:
	sudo -u postgres psql
	CREATE DATABASE ${DATABASE_NAME};
	CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
	ALTER ROLE ${DB_USER} SET client_encoding TO 'utf8';
	ALTER ROLE ${DB_USER} SET default_transaction_isolation TO 'read committed';
	ALTER ROLE ${DB_USER} SET timezone TO 'UTC';
	GRANT ALL PRIVILEGES ON DATABASE ${DATABASE_NAME} TO ${DB_USER};
	\q

setup_venv:
	mkdir ${PROJECT_DIR}
	cd ${PROJECT_DIR}
	git clone git@github.com:martim-lusofona/class-ping.git
	sudo apt install pipenv
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt update
	sudo apt install python3.12 python3.12-venv python3.12-dev
	pipenv shell
	pipenv install
	

create_pre:
	set -a && source .env && set +a && envsubst < ./Makefile > ./Makefile.new

setup_gunicord_socket:
	sudo nano /etc/systemd/system/gunicorn.socket

setup_gunicord_service:
	sudo nano /etc/systemd/system/gunicorn.service

start_gunicord:
	sudo systemctl start gunicorn.socket
	sudo systemctl enable gunicorn.socket

setup_nginx:
	sudo nano /etc/nginx/sites-available/${PROJECT_NAME}
	sudo ln -s /etc/nginx/sites-available/${PROJECT_NAME} /etc/nginx/sites-enabled
	sudo nginx -t
	sudo systemctl restart nginx
	sudo ufw allow 'Nginx Full'