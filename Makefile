include .env

build:
	docker-compose build

up-daemon:
	docker-compose up -d

up:
	docker-compose up

start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose stop && docker-compose start

migrations:
	docker exec $(PROJECT_NAME)_app /bin/sh -c "python manage.py makemigrations"

migrate:
	docker exec $(PROJECT_NAME)_app /bin/sh -c "python manage.py migrate"

superuser:
	docker exec -it $(PROJECT_NAME)_app /bin/sh -c "python manage.py createsuperuser"

startapp:
	docker exec $(PROJECT_NAME)_app /bin/sh -c "mkdir apps/tmp"
	docker exec $(PROJECT_NAME)_app /bin/sh -c "python manage.py startapp $(app_name) apps/tmp"
	docker exec $(PROJECT_NAME)_app /bin/sh -c "mv apps/tmp apps/$(app_name)"

test:
	docker exec $(PROJECT_NAME)_app /bin/sh -c "python manage.py test $(app_name)"

collectstatic:
	docker exec $(PROJECT_NAME)_app /bin/sh -c "python manage.py collectstatic --noinput"

loaddata:
	docker exec $(PROJECT_NAME)_app /bin/sh -c "python manage.py populate"

showmigrations:
	docker exec $(PROJECT_NAME)_app /bin/sh -c "python manage.py showmigrations $(app_name)"

django-shell:
	docker-compose run web python manage.py shell_plus

shell-nginx:
	docker exec -ti $(PROJECT_NAME)_nginx /bin/sh

shell-web:
	docker exec -ti $(PROJECT_NAME)_app /bin/bash

shell-db:
	docker exec -ti $(PROJECT_NAME)_db /bin/bash

log-nginx:
	docker-compose logs nginx

log-web:
	docker-compose logs web

log-db:
	docker-compose logs db
