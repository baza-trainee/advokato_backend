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
	docker compose up -d postgres redis celery web

init-postgres:
	docker compose up -d postgres

db-init:
	docker compose exec web flask db init

db-migrate:
	docker compose exec web flask db migrate

db-upgrade:
	docker compose exec web flask db upgrade

open-redis:
	docker exec -it $$(docker compose ps -q redis) redis-cli -p 9351

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

prod: down build run
	docker compose exec web flask db upgrade
	docker compose exec web flask init
	@echo "Init done, all containers running"

backup:
	@echo "* * * * * cd $(PWD) && python3 scripts/backup.py" | crontab -
	@echo "backup script started"

stop_backup:
	crontab -r

restore:
	python3 scripts/restore.py
