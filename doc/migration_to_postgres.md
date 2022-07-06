## Migration to PostgreSQL
### Docker

1. Update to last MariaDB version :
```
git fetch --all --tags
git checkout tags/v0.1.06-premigrate
docker-compose up --build backend
# Wait until all containers start, and database schema update
# Stop docker (ctrl-c)
```
2. Migrate
```
git checkout tags/v0.1.07-migration
docker-compose up --abort-on-container-exit --build backend
# Data will be migrate to PostgreSQL. Logs in log/migration.log
```
3. Update to last version
```
git checkout main
docker-compose up
```
4. Clean old data

`db/` folder contains MariaDB database. If migration is done correctly, it can be deleted.
### Standalone installation
1. Update to last MariaDB version :
```
sudo systemctl stop tranquility
git fetch --all --tags
git checkout tags/v0.1.06-premigrate
cd backend
./local.alembic_upgrade.sh
```
2. Install PostgreSQL, ocnfigure database and user:
```
apt install postgresql
sudo -u postgres psql
CREATE USER tr_user WITH PASSWORD 'tr_password';
CREATE DATABASE tr_db ENCODING='utf8' TEMPLATE template0;
GRANT ALL PRIVILEGES ON DATABASE tr_db TO tr_user;
EXIT
```
3. Migrate
```
git checkout tags/v0.1.07-migration
```
Edit .env.local, add PostgreSQL enviroment variables POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_USER, POSTGRES_SERVER (see .env for example).
```
cd backend
./local.migrate.sh
# Data will be migrate to PostgreSQL, check console for logs.
```
4. Update to last version
```
git checkout main
cd backend
./local.alembic_upgrade.sh
sudo systemctl start tranquility
```
If migration is done correctly, MariaDB package and data files can be removed.

