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
root@dokku$ dokku git:set thedatalab deploy-branch main
root@dokku$ dokku plugin:install https://github.com/dokku/dokku-postgres.git
root@dokku$ dokku postgres:create thedatalab_production 
root@dokku$ dokku postgres:link thedatalab_production thedatalab
local$ git clone git@github.com:ebmdatalab/thedatalab.git
local$ cd thedatalab
local$ git remote add dokku dokku@DOKU_HOSTNAME:thedatalab
local$ git push dokku main
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
DJANGO_MEDIA_ROOT=/code/storage/media
MAILGUN_API_KEY=abcde_1234
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

## Nginx config tweaks

### increase  max_upload_size

Default is 1Mb, photos for blogs are often 5+Mb. See this method from [the dokku docs](http://dokku.viewdocs.io/dokku/configuration/nginx/#customizing-via-configuration-files-included-by-the-default-tem)

```bash
root@dokku$ mkdir /home/dokku/thedatalab/nginx.conf.d/
root@dokku$ echo 'client_max_body_size 50m;' > /home/dokku/thedatalab/nginx.conf.d/upload.conf
root@dokku$ chown -R dokku:dokku /home/dokku/thedatalab/nginx.conf.d/
root@dokku$ service nginx reload
```

### Add redirects from old urls to new urls

#### Redirect paths

Conf file is in `/deploy/redirects.conf`, but it needs to be outside of the container to add it to the nginx setup, so you'll need to copy the file to the dokku host manually.

```bash
root@dokku$ cp MY_REDIRECTS_CONF /home/dokku/thedatalab/nginx.conf.d/redirects.conf
root@dokku$ chown -R dokku:dokku /home/dokku/thedatalab/nginx.conf.d/
root@dokku$ service nginx reload
root@dokku$ dokku ps:rebuild thedatalab
```

#### Redirect domain name

We can use the dokku plugin set up earlier:

```bash
$ dokku domains:add thedatalab ebmdatalab.net www.ebmdatalab.net
$ dokku redirect:set thedatalab ebmdatalab.net www.thedatalab.org
$ dokku redirect:set thedatalab www.ebmdatalab.net www.thedatalab.org
```

## https

* Currently using CloudFlare "flexible"
  * site available https, encrypted between browser & CloudFlare
* create CloudFlare page rule
  * `www.thedatalab.org/*` -> `Always Use HTTPS`

## Backup

### Install gsutil on dokku host server

As per [google's instructions](https://cloud.google.com/storage/docs/gsutil_install#deb):

```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get install apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
gcloud init
```

* Default config:
  * region: `europe-west2-a`
  * project: _TEST_PROJECT_NAME_
    * we can override with `--project _REAL_PROJECT_NAME_` if necessary

Very simple backup script, which you could run from cron:

```bash
#!/bin/bash
d=$(date +%Y-%m-%d)
google_cloud_storage_url="gs://my_gs_bucket_name"

dokku postgres:export thedatalab_production > /root/thedatalab_backup/thedatalab_production.dump
gsutil cp /root/thedatalab_backup/thedatalab_production.dump $google_cloud_storage_url/thedatalab_production-$d.dump
tar -cf /root/thedatalab_backup/thedatalab_storage.tar /var/lib/dokku/data/storage/thedatalab
gsutil cp /root/thedatalab_backup/thedatalab_storage.tar $google_cloud_storage_url/thedatalab_storage-$d.tar
```
