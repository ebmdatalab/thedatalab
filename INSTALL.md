# thedatalab.org - Install guide
## Dokku setup

http://dokku.viewdocs.io/dokku/deployment/application-deployment/

### Add a deployment user

```bash
root@dokku$ cat > newperson_rsa.pub
root@dokku$ dokku ssh-keys:add newperson /root/newperson_rsa.pub
```

### Create application

```bash
root@dokku$ dokku apps:create thedatalab
root@dokku$ dokku plugin:install https://github.com/dokku/dokku-postgres.git
root@dokku$ dokku postgres:create thedatalab_production 
root@dokku$ dokku postgres:link thedatalab_production thedatalab
local$ git clone git@github.com:ebmdatalab/thedatalab.git
local$ cd thedatalab
local$ git remote add dokku dokku@DOKU_HOSTNAME:thedatalab
local$ git push dokku master
```

### Use of Dockerfile

[While Dokku normally defaults to using Heroku buildpacks, you can also use \[a\] Dockerfile](http://dokku.viewdocs.io/dokku~v0.21.4/deployment/methods/dockerfiles/)

### Configure environment

The app expects the following environment vars:

```bash
DJANGO_SETTINGS_MODULE=thedatalab.settings.production
POSTGRES_DATABASE=ebmdatalab_production
POSTGRES_USER=ebmdatalab_production
POSTGRES_PASSWORD=asdasd123
POSTGRES_HOST=pgdbhost
POSTGRES_PORT=5432
EMAIL_HOST=1.2.3.4
DJANGO_MEDIA_ROOT=/code/storage/media
```

#### Django

```bash
dokku config:set thedatalab DJANGO_SETTINGS_MODULE=thedatalab.settings.production
```

#### PostgreSQL

Dokku auto-generates `DATABASE_URL`, but the app expects `POSTGRES_*`

```bash
dokku config:set thedatalab POSTGRES_DATABASE=mydb ...etc...
```

* TODO: load the database


#### Persistent storage

http://dokku.viewdocs.io/dokku/advanced-usage/persistent-storage/

Django assets:

```bash
root@dokku$ mkdir -p /var/lib/dokku/data/storage/thedatalab/webroot/static/
root@dokku$ chown -R www-data:dokku /var/lib/dokku/data/storage/thedatalab
root@dokku$ dokku storage:mount thedatalab /var/lib/dokku/data/storage/thedatalab/webroot:/code/webroot
```

media:

```bash
root@dokku$ mkdir -p /var/lib/dokku/data/storage/thedatalab/storage/media
root@dokku$ cp $ALL_MY_FILES /var/lib/dokku/data/storage/thedatalab/storage/media
root@dokku$ chown -R www-data:dokku /var/lib/dokku/data/storage/thedatalab
root@dokku$ dokku storage:mount thedatalab /var/lib/dokku/data/storage/thedatalab/storage:/code/storage
root@dokku$ dokku config:set thedatalab DJANGO_MEDIA_ROOT=/code/storage/media
```

