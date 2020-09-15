# thedatalab.org - Install guide
## Dokku setup

http://dokku.viewdocs.io/dokku/deployment/application-deployment/

### Add a deployment user

Get access to the dokku repo, if you're new:

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
dokku$ dokku config:set thedatalab POSTGRES_DATABASE=mydb ...etc...
```

### Load database

Check out the [dokku-postgres docs](https://github.com/dokku/dokku-postgres). The easiest way is if you have a postgresql dump from the dokku server, but if you have an SQL file you can access the server directly by entering its container:

```bash
dokku$ dokku postgres:enter thedatalab_production
dokku-postgres$ psql -U postgres -f ebmdatalab.sql
```

### Persistent storage

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

### Ports & domains

```bash
$ dokku proxy:ports-add thedatalab http:80:8000
$ dokku domains:add thedatalab new.thedatalab.org 
$ dokku domains:add thedatalab thedatalab.org www.thedatalab.org 
```

## Redirect from root domain to www. 

This plugin does 301 redirects

```bash
$ dokku plugin:install https://github.com/dokku/dokku-redirect.git
$ dokku redirect:set thedatalab thedatalab.org www.thedatalab.org
```

## Nginx config - increase  max_upload_size

Default is 1Mb, photos for blogs are often 5+Mb. See this method from [the dokku docs](http://dokku.viewdocs.io/dokku/configuration/nginx/#customizing-via-configuration-files-included-by-the-default-tem)

```bash
root@dokku$ mkdir /home/dokku/thedatalab/nginx.conf.d/
root@dokku$ echo 'client_max_body_size 50m;' > /home/dokku/thedatalab/nginx.conf.d/upload.conf
root@dokku$ chown -R dokku:dokku /home/dokku/thedatalab/nginx.conf.d/
root@dokku$ service nginx reload
```

## https

TODO!
