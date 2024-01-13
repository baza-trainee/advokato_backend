from datetime import datetime
import os

DB_CONTAINER = "postgres_db"
WEB_CONTAINER = "web"
DATABASE_URI = os.environ["DATABASE_URI"]

BACKUP_DIR = "backup-postgres-advokato"
STATIC_BACKUP_DIR = "backup-static-advokato"

TIME_FORMAT = "%Y%m%d_%H%M%S"

if not os.path.exists(BACKUP_DIR):
    print("Backup directory does not exist. Exiting.")
    exit(1)

BACKUPS = sorted(
    os.listdir(BACKUP_DIR),
    key=lambda x: datetime.strptime(x, f"backup_{TIME_FORMAT}.sql"),
    reverse=True,
)
BACKUPS_STATIC = sorted(
    os.listdir(STATIC_BACKUP_DIR),
    key=lambda x: datetime.strptime(x, f"static_{TIME_FORMAT}"),
    reverse=True,
)

if not BACKUPS:
    print("No backup files found in the directory. Exiting.")
    exit(1)

print("Оберіть backup-файл зі списку, для відновлення бази даних. Введіть цифру:")
for i, backup in enumerate(BACKUPS, start=1):
    print(f"{i} - {backup}")

choice = int(input("Ваш вибір: "))

# db
os.system(
    f"docker exec {DB_CONTAINER} psql {DATABASE_URI} -c 'DROP SCHEMA public CASCADE;'"
)
os.system(f"docker exec {DB_CONTAINER} psql {DATABASE_URI} -c 'CREATE SCHEMA public;'")
os.system(
    f"docker exec -i {DB_CONTAINER} psql {DATABASE_URI} < {BACKUP_DIR}/{BACKUPS[choice - 1]}"
)

# media
os.system(f"docker exec -it {WEB_CONTAINER} rm -r /code/calendarapi/static/media")

os.system(
    f"cd {STATIC_BACKUP_DIR}/{BACKUPS_STATIC[choice - 1]} && docker cp . {WEB_CONTAINER}:/code/calendarapi/static/media/"
)
