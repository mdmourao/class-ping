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
	sudo apt install python3-pip
	pip install pipenv --user

create_pre:
	set -a && source .env && set +a && envsubst < ./Makefile > ./Makefile.new
