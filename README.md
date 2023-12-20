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


6. Create a `.env` file and set the necessary environment variables:

    <details class="custom-details">
    <summary><b>API settings</b></summary>
    <p class="custom-details-description"><i>Variable for configuring API.</i></p>

    <b class="variable-name">FLASK_ENV</b>=<span class="variable-value">development</span><br>
    <b class="variable-name">FLASK_APP</b>=<span class="variable-value">calendarapi.app:create_app</span><br>
    <b class="variable-name">SECRET_KEY</b>=<span class="variable-value">the_most_secret_key_in_the_world</span><br>
    <b class="variable-name">ADMIN_DEFAULT_LOGIN</b>=<span class="variable-value">admin</span><br>
    <b class="variable-name">ADMIN_DEFAULT_PASSWORD</b>=<span class="variable-value">admin</span><br>
    <b class="variable-name">MAIN_PAGE_URL</b>=<span class="variable-value">http://yourfrontend.com/main</span><br>

    </details>

    <details class="custom-details">
    <summary><b>DB settings</b></summary>
    <p class="custom-details-description"><i>Variables for database and the project configuration.</i></p>

    <b>DATABASE_URI</b>=<span class="variable-value">postgresql://admin:admin@postgres:5432/calendarapi</span><br>
    </details>

    <details class="custom-details">
    <summary><b>Docker settings</b></summary>
    <p class="custom-details-description"><i>Variable for configuring Docker containers.</i></p>

    <b class="variable-name">POSTGRES_DB</b>=<span class="variable-value">calendarapi</span><br>
    <b class="variable-name">POSTGRES_USER</b>=<span class="variable-value">admin</span><br>
    <b class="variable-name">POSTGRES_PASSWORD</b>=<span class="variable-value">admin</span>
    </details>

    <details class="custom-details">
    <summary><b>Redis and Celery settings</b></summary>
    <p class="custom-details-description"><i>Variable for configuring Redis and Celery containers.</i></p>

    <b class="variable-name">REDIS_PASS</b>=<span class="variable-value">strong_password123</span><br>
    <b class="variable-name">REDIS_PORT</b>=<span class="variable-value">1111</span><br>
    <b class="variable-name">CELERY_BROKER_URL</b>=<span class="variable-value">redis://:$(echo $REDIS_AUTH)@redis:$(echo $REDIS_PORT)</span><br>

    <b class="variable-name">CELERY_RESULT_BACKEND_URL</b>=<span class="variable-value">redis://:$(echo $REDIS_AUTH)@redis:$(echo $REDIS_PORT)</span>
    </details>


    <details class="custom-details">
    <summary><b>Mail settings</b></summary>
    <p class="custom-details-description"><i>Variable for configuring Mail service.</i></p>

    <b class="variable-name">MAIL_SERVER</b>=<span class="variable-value">smtp.gmail.com</span><br>
    <b class="variable-name">MAIL_PORT</b>=<span class="variable-value">587</span><br>
    <b class="variable-name">MAIL_USERNAME</b>=<span class="variable-value">your_mail@gmail.com</span><br>
    <b class="variable-name">MAIL_PASSWORD</b>=<span class="variable-value">your_mail_api_key</span>
    </details>

    <details class="custom-details">
    <summary><b>Cloudinary settings</b></summary>
    <p class="custom-details-description"><i>Variable for configuring Cloudinary service.</i></p>

    <b class="variable-name">CLOUD_NAME</b>=<span class="variable-value">yourcloudname</span><br>
    <b class="variable-name">API_KEY</b>=<span class="variable-value">yourapikey</span><br>
    <b class="variable-name">API_SECRET</b>=<span class="variable-value">yourapisecret</span><br>
    </details>

7. Initialize and start the containers:

    ```
    make prod
    ```

After successfully executing this command, you should have `5 Docker containers` up and running.

Since development is carried out within the container, the migrations folder is also created inside it. Therefore, in case of changes to the database model, it is necessary to run the commands `make db-migrate` and `make db-upgrade`. This will allow performing migrations inside the containers.

To debug the code, you can view the container logs using the command `docker logs <container_name>`. The container is automatically restarted after saving changes to the code, or manually using the `make dev` or `make build run` commands."

## Containers

<div style="text-align: right;">
    <div style="float: left; padding-right: 15px; padding-top: 10px">
        <img src="https://raw.githubusercontent.com/docker/compose/master/logo.png" alt="Docker Compose" align="left" width="200">
    </div>
    <br>
</div>

- `web` - The Flask application container.
- `postgres` - The PostgreSQL database container.
- `redis` - The Redis container used for caching and storing the results of asynchronous tasks.
- `celery` - The Celery task worker container.
- `flower` - The Flower Celery task monitoring tool container.


## Run locally
If you need to run the application locally, stop the `web` container, change the database address in the `.env` file. 
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

- `init`: Postgres container initialization, building, creating the admin user and startup.
- `build:` Builds Docker images.
- `run`: Starts Docker containers.
- `db-migrate`: Create migration file inside the container.
- `db-upgrade`: Apply migrations inside the container.
- `test`: Run project tests.
- `lint`: Run the linter to check the code.
- `tox`: Code linting with subsequent testing.
- `prod`: Run the project with all containers.
- `clean`: Clean Python-related files.
