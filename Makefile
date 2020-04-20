help:
	@echo "Docker Compose Help"
	@echo "-----------------------"
	@echo ""
	@echo "Run tests and checks to ensure current state is good:"
	@echo "    make check"
	@echo ""
	@echo "If tests pass, add fixture data and start up the app:"
	@echo "    make begin"
	@echo ""
	@echo "Really, really start over:"
	@echo "    make clean"
	@echo ""
	@echo "See contents of Makefile for more targets."

begin: migrate start

start:
	@docker-compose up -d
stop:
	@docker-compose stop

status:
	@docker-compose ps

restart: stop start

clean: stop
	@docker-compose rm --force
	@find . -name \*.pyc -delete

build:
	@docker-compose build app

test:
	@docker-compose run --rm app python ./manage.py test 

lint:  
	@docker-compose run app flake8

django_check: 
	@docker-compose run --rm app python ./manage.py check

check:  build test lint django_check

migrate:
	@docker-compose run --rm app python ./manage.py migrate

createsuperuser:
	@docker-compose run --rm app python ./manage.py createsuperuser

cli:
	@docker-compose run --rm app bash

tail:
	@docker-compose logs -f

.PHONY: start stop status restart clean build test migrate cli tail
