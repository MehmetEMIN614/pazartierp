.PHONY: setup migrate test

setup:
	sh setup.sh

migrate:
	python manage.py migrate

test:
	python manage.py test