
test:
	poetry run pytest --capture=no --benchmark-skip -sx cashbackapi

runserver:
	python manage.py runserver

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

generate_secret_key:
	python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
