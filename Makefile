.PHONY: init init-migration down build run db-migrate test tox prod drop_db auto_backup backup restore prune frontend_build frontend_export

BACKUP_COMMAND := 0 1 * * * cd "$(PWD)" && python3 scripts/backup.py

prod: down build run

init: down run init-postgres
	sleep 3
	flask db upgrade
	flask init
	flask --debug run --port=5000
	@echo "Init done, postgres container running"

build:
	docker compose build

down:
	docker compose down

run:
	docker compose up -d

init-postgres:
	docker compose up -d postgres

db-init:
	docker compose exec backend flask db init

db-migrate:
	docker compose exec backend flask db migrate

db-upgrade:
	docker compose exec backend flask db upgrade

open-redis:
	docker exec -it $$(docker compose ps -q redis) redis-cli -p 9351

test:
	docker compose stop celery # stop celery to avoid conflicts with celery tests
	docker compose start rabbitmq redis # ensuring both redis and rabbitmq are started
	docker compose run --rm -v "$(PWD)/tests:/code/tests:ro" backend tox -e test -- -v
	docker compose start celery

tox:
	docker compose stop celery # stop celery to avoid conflicts with celery tests
	docker compose start rabbitmq redis # ensuring both redis and rabbitmq are started
	docker compose run --rm -v $(PWD)/tests:/code/tests:ro backend tox -e py311
	docker compose start celery

lint:
	docker compose run --rm backend tox -e lint

clean:
	sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs sudo rm -rf

auto_backup:
	@if crontab -l ; then \
		crontab -l > mycron ; \
	else \
		touch mycron ; \
	fi
	@echo '$(BACKUP_COMMAND)' >> mycron
	@crontab mycron
	@rm mycron
	@echo "Backup script added to cron"

backup:
	python3 scripts/backup.py
	@echo "Backup complete"
	
stop_backup:
	crontab -l | grep -v '$(BACKUP_COMMAND)' | crontab -

restore:
	python3 scripts/restore.py

frontend_build:
	if [ -d dist.tar.xz ]; then \
		sudo rm -rf dist.tar.xz; \
	fi
	tar -cJvf dist.tar.xz dist

frontend_export:
	if [ -d /var/www/school/dist ]; then \
		sudo rm -rf /var/www/advokato/dist; \
	fi
	sudo mkdir -p /var/www/advokato/
	sudo tar -xJvf dist.tar.xz -C /var/www/advokato/


drop_db: down
	if docker volume ls -q | grep -q $$(basename "$$(pwd)")_postgres_data; then \
		docker volume rm $$(basename "$$(pwd)")_postgres_data; \
		echo "successfully drop_db command";\
	fi
	sudo rm -rf ./calendarapi/static/media

prune: down
	docker system prune -a
	docker volume prune -a
