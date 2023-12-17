.PHONY: init init-migration down build run db-migrate test tox

init: down init-postgres
	sleep 2
	flask db upgrade
	flask init
	flask --debug run
	@echo "Init done, postgres container running"

build:
	docker compose build

down:
	docker compose down

run:
	docker compose up -d postgres redis celery flower web

init-postgres:
	docker compose up -d postgres

db-init:
	docker compose exec web flask db init

db-migrate:
	docker compose exec web flask db migrate

db-upgrade:
	docker compose exec web flask db upgrade

open-redis:
	docker exec -it $$(docker compose ps -q redis) redis-cli

test:
	docker compose stop celery # stop celery to avoid conflicts with celery tests
	docker compose start rabbitmq redis # ensuring both redis and rabbitmq are started
	docker compose run --rm -v "$(PWD)/tests:/code/tests:ro" web tox -e test -- -v
	docker compose start celery

tox:
	docker compose stop celery # stop celery to avoid conflicts with celery tests
	docker compose start rabbitmq redis # ensuring both redis and rabbitmq are started
	docker compose run --rm -v $(PWD)/tests:/code/tests:ro web tox -e py311
	docker compose start celery

lint:
	docker compose run --rm web tox -e lint

clean:
	sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs sudo rm -rf

dev:
	# sed -i 's/:\/\/admin:admin@postgres:/:\/\/admin:admin@localhost:/g' .flaskenv
	# @if [ -d "migrations" ]; then \
	# 	rm -r migrations; \
	# fi
	# docker compose down
	# docker compose build postgres
	# docker compose up -d postgres
	# flask db init
	# flask db migrate
	# flask db upgrade
	# flask init
	flask --debug run

prod: down build run
	docker compose exec web flask db init
	docker compose exec web flask db migrate
	docker compose exec web flask db upgrade
	docker compose exec web flask init
	@echo "Init done, all containers running"