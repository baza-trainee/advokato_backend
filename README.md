![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-blue.svg)](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
[![Docker-compose](https://img.shields.io/badge/docker-compose-orange.svg)](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
![Linux (Ubuntu)](https://img.shields.io/badge/linux-ubuntu-green.svg)
## Installation

To run the project, you will need [Docker](https://www.docker.com/) installed. Follow these steps to install and run the project:

1. Create a new folder for your project.

2. Open the project in an IDE

3. Initialize Git

    ```
    git init
    ```
4. Add the remote repository
    ```
    git remote add origin https://github.com/baza-trainee/python-calendar.git
    ```
5. Sync with the remote repository

    ```
    git pull origin dev
    ```


6. Create a `.flaskenv` file if it does not already exist and set the necessary environment variables:

    ```
    FLASK_ENV=development
    FLASK_APP=calendarapi.app:create_app
    SECRET_KEY=changeme
    DATABASE_URI=postgresql://admin:admin@postgres:5432/calendarapi

    CELERY_BROKER_URL=amqp://guest:guest@rabbitmq
    CELERY_RESULT_BACKEND_URL=redis://redis

    ```
7. Create a `.testenv` file if it does not already exist and set the necessary environment variables::

    ```
    # using in container
    SECRET_KEY=testing
    DATABASE_URI=sqlite:///:memory:
    CELERY_BROKER_URL=amqp://guest:guest@localhost/
    CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/

    ```
8. Initialize and start the containers:

    ```
    make init
    ```

After successfully executing this command, you should have `7 Docker containers` up and running.

Since development is carried out within the container, the migrations folder is also created inside it. Therefore, in case of changes to the database model, it is necessary to run the commands `make db-migrate` and `make db-upgrade`. This will allow performing migrations inside the containers.

To debug the code, you can view the container logs using the command `docker logs <container_name>`. The container is automatically restarted after saving changes to the code, or manually using the `make dev` or `make build run` commands."

## Containers

<div style="text-align: right;">
    <div style="float: left; padding-right: 15px; padding-top: 10px">
        <img src="https://raw.githubusercontent.com/docker/compose/master/logo.png" alt="Docker Compose" align="left" width="200">
    </div>
    <br>
    <br>
    <br>
</div>

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

## Testing


Just like everything else in the project, testing is also highly automated and easy to run with a single command. The project's `Makefile` contains three commands for testing and maintaining code quality.

Each of these commands creates a separate testing environment (a separate container) in which it installs the necessary dependencies and performs specific actions.


- `make test`: Creates a container for running all the tests, first stopping Celery to avoid conflicts and ensure test cleanliness. If the tests are successful, the container created for this purpose will be removed, and Celery will be restarted.

- `make lint`: Creates a container to check the code for compliance with PEP standards and helps maintain a consistent and easily readable code style.

- `make tox`: Essentially, this is a combination of the first and second commands. It creates a container, checks the code style, and then runs all the tests. After successful completion, the container is automatically removed.

You can also test the project locally by installing the dependencies from the `requirements_tests.txt` file.



## Monitoring
- The application with the Swagger documentation will be available at:
```
http://localhost:5000/swagger-ui
```
- Access to the admin panel for managing the database and schedule is available here
```
http://localhost:5000/admin
```
The **password** and **login** to the main user of the admin panel can be changed in the file: `.flaskenv`
```
ADMIN_DEFAULT_LOGIN = admin
ADMIN_DEFAULT_PASSWORD = admin
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
