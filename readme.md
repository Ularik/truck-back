# Django Starter Project

[RU](readme_ru.md)

Check out the ["About the Project" document](about.md)


# Installation

## back

### Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd app
python manage.py runserver
```
Additional virtual environment commands:
```bash
source venv/bin/activate
deactivate
```
For livereload, run additionally:
```bash
python manage.py livereload
```

### Deployment Script

To enable auto-deployment, run the **deploy.sh** script.

Give execute permission:
```bash
chmod ugo+x deploy.sh
```

### Example Bash Script to Launch Deployment Script

You can place this script in the user's home directory for quick deployment launch.

To find the folder path:
```bash
pwd
```
Navigate to the home directory:
```bash
cd ~
```
To create a file:
```bash
touch {file_name}
```
Script to launch the deployment script from the home directory:
```bash
#!/bin/bash
cd {project_folder_path}
chmod ugo+x deploy.sh
./deploy.sh
```
Name the launch file by project or user to avoid confusion when working with many projects:
```bash
touch myproject
```
Launch:
```bash
./myproject
```
This will start deployment while staying in the home directory.

### Example Script to Activate Environment

**venv** (or another env folder name)
Place this script in the home directory for quick activation.
Example name: **go**
```bash
touch go
```
Activation script:
```bash
#!/bin/bash
. {project_folder_path}/venv/bin/activate
cd {project_folder_path}/
```
**Important:** Create the virtual environment and install dependencies first:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Run script:
```bash
. go
```
Grant execution permissions to the script:
```bash
chmod ugo+x {file_name}
```

### Example for Copying a Database to a Clean One
```bash
#!/bin/bash
echo 'exp bd_prod'
PGPASSWORD=111111 pg_dump -U user_bd my_bd -f the_backup.sql

echo 'imp bd_dev'
PGPASSWORD=22222 psql -U user_dev -d bd_dev -f  the_backup.sql
```

### Using the Deployment Script

Install git on the server.
Then clone the repository into the project root.

Example cloning from GitLab using a personal access token:

Use the following template:
1. **group** - repository group, visible in URL (gitlab.com/{group}/my_app)
2. **token** - personal access token (Settings -> Access Tokens)
3. **app_name** - repository name
```bash
git clone https://{group}:{token}@gitlab.com/{group}/{app_name}.git .
```
The dot at the end clones into the current (empty) directory.

***IMPORTANT!***
Checkout to the desired branch:
```bash
git branch -a
git rev-parse --abbrev-ref HEAD
git checkout {branchname}
```

Script workflow:
1. Prepares git by cleaning up, then fetches branch.
2. Installs requirements.txt dependencies.
3. Runs migrations.
4. Runs autotests.
5. Console shows logs for inspection.
6. If all good, restart or rebuild docker-compose.

## Key Notes

1. Folders app, media, logs are mounted into Docker:
```yaml
volumes:
  - ./app:/usr/www/app/
  - ./media:/usr/www/media/
  - ./logs:/usr/www/logs/
```
This allows live code/file updates between Docker and host.

2. Ports are set in the .env file.
3. Django modes are controlled via the DEV variable.
4. Docker supports: Django (app), Celery (worker, beats), Redis, Postgres, Flower, PGAdmin. Comment out unneeded services.

Sample **.env**:
```env
DEV=true
APP_PORT=8001
FLOWER_USERNAME=user
FLOWER_PASSWORD=1
FLOWER_PORT=9090

# DEV DB
POSTGRES_DB=mydb
POSTGRES_USER=root
POSTGRES_PASSWORD=root
POSTGRES_PORT=5432
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin
PGADMIN_PORT=5050
```

**DEV** values: *true*, *false*, *local*
- *true*: uvicorn with hot reload
- *local*: runserver mode (for local Docker without nginx)
- *false*: production mode

APP_PORT – app access port

FLOWER_* – Flower web interface config

DEV DB section – launches DB with PGAdmin

## Nginx Config Example
Set port from .env and site path:
```nginx
location /static {
    alias $root_path/app/static;
}
location /media {
    alias $root_path/media;
}

location / {
    proxy_pass http://127.0.0.1:{port from env};
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $server_name;
    location ~* ^.+\.(jpg|jpeg|gif|png|svg|js|css|mp3|ogg|mpe?g|avi|zip|gz|bz2?|rar|swf|webp|woff|woff2)$ {
        expires 24h;
    }
}
```

In the project folder:
`settings_local.py` – constants for launch, sample in `settings_local.py.txt`

## front

In the **/front** folder:
Starter Vue.js project using PrimeVue:
https://primevue.org/

In the **/front-template** folder:
Starter template using Metronic 8:
https://preview.keenthemes.com/metronic8/demo1/index.html?mode=light

Also used as a Django template.

> These front-end folders are optional.

# Additional

## Common Django Commands
```bash
django-admin startproject project .
python manage.py startapp company
python manage.py createsuperuser

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
python manage.py collectstatic

python manage.py inspectdb

python manage.py test --keepdb
python manage.py test company.tests.test_dis --keepdb
```

## Change Python Version
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12-full
```
Extra modules:
```bash
sudo apt install python3.12-{tk,dev,dbg,venv,gdbm,distutils}
```
Full install:
```bash
sudo apt install python3.12-full
```
Update system Python:
```bash
ls /usr/bin/python*

rm /usr/bin/python
ln -s /usr/bin/python3.12 /usr/bin/python

sudo rm /usr/bin/pip
sudo ln -s /usr/bin/pip3.12 /usr/bin/pip
```

## Docker Commands
```bash
docker ps
docker exec -it my_app_1 bash

docker-compose restart
docker-compose up --build
docker-compose build --no-cache
docker-compose up -d
docker-compose down
docker-compose ps
docker ps --filter "name=app" --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}"
```
Clean up:
```bash
docker system prune -f
```
Docker access permissions:
```bash
sudo usermod -aG docker {new_user}

sudo chmod +666 /var/run/docker.sock

ls -l /var/run/docker.sock
```
Docker mirror:
```bash
nano /etc/docker/daemon.json

{ "registry-mirrors" : [ "https://mirror.gcr.io" ] }

sudo service docker restart
```

## Run Without Docker

Run as a service:
```bash
sudo nano /etc/systemd/system/uvicorn.service
```
```ini
[Unit]
Description=Uvicorn API
After=network.target

[Service]
User=vds
Group=vds
WorkingDirectory=/var/www/api-express/app
ExecStart=/var/www/api-express/venv/bin/uvicorn project.asgi:application --host 127.0.0.1 --port 8001 --reload --reload-include *.html
Restart=always
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
Reload and check status:
```bash
systemctl daemon-reload
sudo systemctl status api-express.service
sudo journalctl -u api-express.service -f
```
Grant service permissions:
```bash
sudo visudo

user_web ALL=(ALL) NOPASSWD: /bin/systemctl start unicorn_my_app.service
user_web ALL=(ALL) NOPASSWD: /bin/systemctl stop unicorn_my_app.service
user_web ALL=(ALL) NOPASSWD: /bin/systemctl restart unicorn_my_app.service
```
No password prompt when using sudo.

Log tailing:
```bash
tail -f uvicorn.log
```

## Redis
Clear all:
```bash
docker exec -i cpexpcardru-redis-1 redis-cli FLUSHALL
```

## PostgreSQL
Enable plugins:
```bash
sudo -u postgres psql -d tanos_test
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

## Used Libraries
1. Well-known: `djangorestframework`, `django-cors-headers`, `psycopg2-binary`, `django-filter`, `requests`

Lesser-known:

2. **livereload** – auto reload on code changes.
https://pypi.org/project/django-livereload-server/
> Great for frontend work. **Disable on prod** (`livereload.middleware.LiveReloadScript`).

3. **db_logger** – logs to DB, viewable in admin panel.
https://pypi.org/project/db-logger/
- Included directly in the project.
- Configured via LOGGING settings as `'db_log'`.
- Depends on `six`.

4. **djangorestframework-simplejwt** – JWT support for DRF.

5. **django-ninja** – Fast async API alternative to DRF.

6. **django-ninja-jwt** – JWT implementation for Ninja.
https://pypi.org/project/django-ninja-jwt/

