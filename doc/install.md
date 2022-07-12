# Installation
## Deployment options

Settings in .env file:
* POSTGRES_USER, POSTGRES_PASSWORD - database access credentials
* POSTGRES_DB - database name
* POSTGRES_SERVER - server IP (should be "pgdb" when using Docker)
* BACKEND_CORS_ORIGINS - comma separated IP address for CORS (needed if frontend and backend have different origin)
* SECRET_KEY - random string to encrypt JWT token
* FIRST_SUPERUSER - first user email
* FIRST_SUPERUSER_PASSWORD - first user password
* VUE_APP_DOMAIN - backend URL
* DEMO_USERS - Maximum number of users for demo-mode (if zero - demo mode is disabled)
* VUE_APP_DEMOMODE - Is demo sign-in enabled?

VUE_APP_DOMAIN and BACKEND_CORS_ORIGINS are used only if frontend and backend are running on different IP addresses or ports. Otherwise keep empty values.

VUE_APP_DEMOMODE and DEMO_USERS are used for demo access, in normal mode both variables should be zero.

## Run in Docker

1. Edit .env file if necessary
2. Run: `docker-compose up`
3. Open `http://[your_server_ip]:8080/` in browser. (login and password in .env file)

To run tests in docker use:
`docker-compose -f docker-compose-tests.yml up --abort-on-container-exit --exit-code-from backend`

## Installation without Docker

Example for Debian/Ubuntu linux.

#### 1. Configure database
Install and configure PostgreSQL:
```
sudo apt install postgresql
sudo -u postgres psql
CREATE USER tr_user WITH PASSWORD 'tr_password';
CREATE DATABASE tr_db ENCODING='utf8' TEMPLATE template0;
GRANT ALL PRIVILEGES ON DATABASE tr_db TO tr_user;
EXIT
```

#### 2. Configure Tranquility

Clone repository to your system, in example used /srv/tranquility directory. Copy .env to .env.local and edit settings.
```
cd /srv
sudo git clone https://github.com/divetoh/tranquility.git
cd tranquility
sudo cp .env .env.local
sudo nano .env.local
```
 Example .env.local:
```
POSTGRES_PASSWORD=tr_password
POSTGRES_DB=tr_db
POSTGRES_USER=tr_user
POSTGRES_SERVER=localhost
BACKEND_CORS_ORIGINS=
SECRET_KEY=MY_RANDOM_SUPER_SECRET_KEY_123456
FIRST_SUPERUSER=admin@test.test
FIRST_SUPERUSER_PASSWORD=admin
VUE_APP_DOMAIN=
```

#### 3. Build frontend
Install nodejs.
```
sudo apt install curl
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs
```

Install dependencies and build frontend.
```
cd frontend
sudo npm install
sudo bash -c ./local.build.sh
cd ..
```
Builded frontend files locate in /srv/tranquility/frontend/dist. 

There is not necessary to install nodejs on production server. You can build frontend on any workstation and copy dist directory to server. 

#### 4. Prepare backend
Install python (3.9 minimum), and python-venv.
```
sudo apt install python3.9 python3.9-venv
```
Run initialization script:
```
cd backend
sudo bash -c ./local.init.sh
cd ..
```
Initialization script:
* try to find python 3.9 or later
* create venv
* install dependencies
* migrate database schema to last revision
* create first user (parameters in .env.local)

You can start uvicorn to check backend:
```
cd backend
./local.start.sh
```
If all works correct, you can open Swagger UI interface in browser: http://[your_server_ip]:5001/docs/

#### 5. Gunicorn configuration


Add user to system, create folders for logs and socket, and set owner:
```
sudo adduser --disabled-password --gecos "" tranquility
sudo mkdir /var/log/tranquility
sudo chown tranquility /var/log/tranquility
sudo mkdir /srv/tranquility/socket
sudo chown tranquility /srv/tranquility/socket
sudo cp /srv/tranquility/backend/gunicorn_conf.py.template /srv/tranquility/backend/gunicorn_conf.py
```

The configuration on gunicorn is in file /backend/unicorn_conf.py, you can edit path to socket or log-files.

Copy system.d configuration file, enable and start gunicorn:
```
sudo cp /srv/tranquility/backend/tranquility.service /etc/systemd/system
sudo systemctl enable tranquility
sudo systemctl start tranquility
```

You can check gunicorn service status:
```
sudo systemctl status tranquility
cat /var/log/tranquility/error_log
```

#### 6. NGINx configuration

Install nginx, edit configuration.
```
sudo apt install nginx
sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-enabled/tranquility
```

Configuration file /etc/nginx/sites-enabled/tranquility example:
```
server {
    listen 80;
    location / {
        try_files $uri $uri/ /index.html;
        root   /srv/tranquility/frontend/dist;
    }

    location /api {
        proxy_pass http://unix:/srv/tranquility/socket/gunicorn.sock;
    }
}
```
Restart nginx.
```
sudo systemctl restart nginx
```
Open `http://[your_server_ip]/` in browser.


#### 7. Afterword
Don't forget to do these basic things:
* Configure SSL, for example [Let's Encrypt](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04)
* Configure log rotation
* Configure database backup
