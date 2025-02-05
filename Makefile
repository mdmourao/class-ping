run:
	python manage.py runserver
makemigrations:
	python manage.py makemigrations
migrate:
	python manage.py migrate
shell:
	python manage.py shell
generate_er:
	python manage.py graph_models -a -o myapp_models.png