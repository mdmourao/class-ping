## DEVELOPMENT
run_dev:
	source .env.dev && python manage.py runserver
makemigrations_dev:
	source .env.dev && python manage.py makemigrations
migrate_dev:
	python manage.py migrate
shell_dev:
	python manage.py shell
generate_er:
	python manage.py graph_models -a -o myapp_models.png


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
