# CalendarAPI

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

description

## Features

- a
- b
- c
- d

## Installation

To run the project, you will need [Docker](https://www.docker.com/) installed. Follow these steps to install and run the project:

1. Clone the repository.

2. Create a `.flaskenv` file and set the necessary environment variables:

```
FLASK_ENV=development
FLASK_APP=calendarapi.app:create_app
SECRET_KEY=changeme
DATABASE_URI=postgresql://admin:admin@postgres:5432/calendarapi

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq
CELERY_RESULT_BACKEND_URL=redis://redis

```
2. Create a `.testenv` file for testing:

```
# using in container
SECRET_KEY=testing
DATABASE_URI=sqlite:///:memory:
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/

```
3. Initialize and start the containers:

```
make init
```

After successfully executing this command, you should have `7 Docker containers` up and running.

## Containers

- `web` - The Flask application container.
- `postgres` - The PostgreSQL database container.
- `pgadmin` - The pgAdmin database management tool container.
- `rabbitmq` - The RabbitMQ message broker container.
- `redis` - The Redis container used for caching and storing the results of asynchronous tasks.
- `celery` - The Celery task worker container.
- `flower` - The Flower Celery task monitoring tool container.

## Run locally
If you need to run the application locally, stop the `web` container, change the database address in the `.flaskenv` file. 
```
DATABASE_URI=postgresql://admin:admin@localhost:5432/calendarapi
```
And then start the application with the `flask run --debug` command.

## Monitoring
- The application with the Swagger documentation will be available at:
```
http://localhost:5000/swagger-ui
```

- You can access pgAdmin at the following URL: 
```
http://localhost:5050
```
- You can access Flower for monitoring Celery tasks at the following URL:
```
http://localhost:5555
```

## Makefile Commands

- `init`: Project initialization, building, creating the admin user and container startup.
- `build:` Builds Docker images.
- `run`: Starts Docker containers.
- `dev`: Reload container with applied changes.
- `db-migrate`: Create migration file inside the container.
- `db-upgrade`: Apply migrations inside the container.
- `test`: Run project tests.
- `lint`: Run the linter to check the code.
- `tox`: Code linting with subsequent testing.
- `clean`: Clean Python-related files.
