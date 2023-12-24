![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-blue.svg)](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
[![Docker-compose](https://img.shields.io/badge/docker-compose-orange.svg)](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
![Linux (Ubuntu)](https://img.shields.io/badge/linux-ubuntu-green.svg)

<h1 align="center" style="color: #B5E5E8;">AC «STATUS» API and Admin Panel</h1>


AC «STATUS» API – a powerful tool for efficient law firm website management. Our application, built on the Flask framework, provides integrated content management website through the user-friendly Flask Admin dashboard.

<h3 align="center">Key Features</h3>

- **Content Management:** Easily add, edit, and delete content on website through an intuitive administrator interface. Whether it's text, images, or other elements – everything is under your control.

- **Flexible Schedule Management:** Our admin panel allows you to control appointments, making it seamless to handle client bookings and staff availability.

- **Client Appointment Booking:** Clients can schedule appointments on the website, choosing specific specialists, convenient dates, and available time slots. The entire process is managed through the admin panel.

- **Email Notifications:** Automated confirmation emails are sent to clients upon successful appointment booking. Additionally, lawyers receive notifications about new scheduled appointments, ensuring everyone stays informed.

- **Reminder Emails:** Clients receive reminder emails on the day of their scheduled appointments.

- **Admin User Management:** The main administrator can create user accounts for staff members, flexible control over their access to various sections of the admin panel.

<h2 align="center" style="color: #B5E5E8;">TECH STACK</h2>

- **Framework:** Flask with FlaskRESTful
- **Database:** PostgreSQL
- **Caching:** Redis for caching and cache invalidation of informational page requests
- **Background Task Execution:** Celery for asynchronous task processing
- **Message Broker:** Redis
- **Task Monitoring:** Flower web interface for monitoring Celery tasks
- **Email Handling:** Flask-Mail for email functionality
- **Admin Panel:** Developed using Flask-Admin

<p align="center">
  <a href="https://flask-restful.readthedocs.io/en/latest/" target="_blank">
    <img src="https://img.shields.io/badge/FlaskRESTful-000000?style=for-the-badge" alt="FlaskRESTful">
  </a>
  <a href="https://www.postgresql.org/" target="_blank">
    <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge" alt="PostgreSQL">
  </a>
  <a href="https://redis.io/" target="_blank">
    <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge" alt="Redis">
  </a>
  <a href="https://docs.celeryproject.org/en/stable/" target="_blank">
    <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge" alt="Celery">
  </a>
  <a href="https://flower.readthedocs.io/en/latest/" target="_blank">
    <img src="https://img.shields.io/badge/Flower-474747?style=for-the-badge" alt="Flower">
  </a>
  <a href="https://pythonhosted.org/Flask-Mail/" target="_blank">
    <img src="https://img.shields.io/badge/Flask--Mail-0078D4?style=for-the-badge" alt="Flask-Mail">
  </a>
  <a href="https://flask-admin.readthedocs.io/en/latest/" target="_blank">
    <img src="https://img.shields.io/badge/Flask--Admin-0078D4?style=for-the-badge" alt="Flask-Admin">
  </a>
</p>

<h2 align="center" style="color: #B5E5E8;">INSTALLATION</h2>

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
    <b class="variable-name">CELERY_BROKER_URL</b>=<span class="variable-value">redis://default:strong_password123@redis:1111</span><br>

    <b class="variable-name">CELERY_RESULT_BACKEND_URL</b>=<span class="variable-value">redis://default:strong_password123@redis:1111</span>
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
    <br>

7. Initialize and start the containers:

    ```
    make prod
    ```

    After successfully executing this command, you should have `5 Docker containers` up and running.<br><br>

8. The project also has an automatic daily backup of the database. To start the script, run the command:
    ```
    make backup
    ```
    A folder named `backup-postgres-db` will be created in the root of your machine, where a new backup file - `backup_TIMESTAMP.sql` - will be created daily at midnight.<br><br>

9. In the future, if necessary, you will be able to restore data from the backup using the command:
    ```
    make restore
    ```
    If there are backup files on your machine, you will be prompted to select one from the list, then press Enter. The script will perform the restoration itself, rolling back the database to the version you selected.<br><br>

Since development is carried out within the container, the migrations folder is also created inside it. Therefore, in case of changes to the database model, it is necessary to run the commands `make db-migrate` and `make db-upgrade`. This will allow performing migrations inside the containers.

To debug the code, you can view the container logs using the command `docker logs <container_name>`. <br>

<h2 align="center" style="color: #B5E5E8;">CONTAINERS</h2>

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
- `redis` - The Redis container used for caching and storing the results of asynchronous tasks.
- `celery` - The Celery task worker container.
- `flower` - The Flower Celery task monitoring tool container.


<h3 align="center" style="color: #B5E5E8;">Run locally</h3>
If you need to run the application locally, stop the `web` container, change the database address in the `.env` file. 

```
DATABASE_URI=postgresql://admin:admin@localhost:5432/calendarapi
```
And then start the application with the `flask run --debug` command.

<h2 align="center" style="color: #B5E5E8;">TESTING</h2>

Just like everything else in the project, testing is also highly automated and easy to run with a single command. The project's `Makefile` contains three commands for testing and maintaining code quality.

Each of these commands creates a separate testing environment (a separate container) in which it installs the necessary dependencies and performs specific actions.


- `make test`: Creates a container for running all the tests, first stopping Celery to avoid conflicts and ensure test cleanliness. If the tests are successful, the container created for this purpose will be removed, and Celery will be restarted.

- `make lint`: Creates a container to check the code for compliance with PEP standards and helps maintain a consistent and easily readable code style.

- `make tox`: Essentially, this is a combination of the first and second commands. It creates a container, checks the code style, and then runs all the tests. After successful completion, the container is automatically removed.

You can also test the project locally by installing the dependencies from the `requirements_tests.txt` file.


<h2 align="center" style="color: #B5E5E8;">MONITORING</h2>

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

<h2 align="center" style="color: #B5E5E8;">MAKEFILE COMMANDS</h2>

- `init`: Initialize the project by bringing up the Postgres container, upgrading the database, and then initializing the application.
- `build:` Build Docker images for the project.
- `down:` Stop and remove all Docker containers.
- `run`: Start Docker containers including Postgres, Redis, Celery, Flower, and the web application.
- `init-postgres`: Start only the Postgres container.
- `db-init`: Initialize the database by running Flask database initialization command inside the web container.
- `db-migrate`: Create a migration file inside the web container.
- `db-upgrade`: Apply database migrations inside the web container.
- `open-redis`: Open a Redis CLI session for the Redis container.
- `test`: Run the project tests using Tox in a web container, and then restart the Celery container.
- `lint`: Run the linter inside the web container to check the code.
- `tox`: Run code linting and tests using Tox in a web container.
- `clean`: Remove Python-related files such as __pycache__, .pyc, and .pyo from the project.
- `prod`: Build Docker images, start containers, initialize the database and initialize the application. This command sets up the project for production use.
- `backup`: Make the backup script executable, add a cron job to run the backup script every midnight.
- `restore`: Make the restore script executable and execute it to restore the database.
