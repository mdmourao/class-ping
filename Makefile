## DEVELOPMENT
run_dev:
	source .env.dev && python manage.py runserver
makemigrations_dev:
	source .env.dev && python manage.py makemigrations
migrate_dev:
	source .env.dev && python manage.py migrate
shell_dev:
	source .env.dev && python manage.py shell
generate_er:
	source .env.dev && python manage.py graph_models -a -o myapp_models.png


## PRODUCTION
check_deploy_prod:
	bash -c 'source .env && python manage.py check --deploy'
makemigrations_prod:
	bash -c 'source .env && python manage.py makemigrations'
migrate_prod:
	bash -c 'source .env && python manage.py migrate'
collectstatic_prod:
	bash -c 'source .env && python manage.py collectstatic'
createsuperuser_prod:
	bash -c 'source .env && python manage.py createsuperuser'
collectstatic:
	python manage.py collectstatic

setup_env:
	exit
	pipenv shell
	pipenv install

deploy_prod:
	bash -c 'source .env && python manage.py makemigrations'
	bash -c 'source .env && python manage.py migrate'
	bash -c 'source .env && python manage.py collectstatic'
	bash -c 'source .env && python manage.py check --deploy'
	sudo systemctl restart gunicorn.service