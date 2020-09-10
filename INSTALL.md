# thedatalab.org - Install guide
## Dokku setup

http://dokku.viewdocs.io/dokku/deployment/application-deployment/

### Add a deployment user

```bash
root@dokku2$ cat > newperson_rsa.pub
root@dokku2$ dokku ssh-keys:add newperson /root/newperson_rsa.pub
```

### Create application

```bash
root@dokku$ dokku apps:create thedatalab
root@dokku$ dokku plugin:install https://github.com/dokku/dokku-postgres.git
root@dokku$ dokku postgres:create thedatalab_production 
root@dokku$ dokku postgres:link thedatalab_production thedatalab
local$ git clone git@github.com:ebmdatalab/thedatalab.git
local$ cd thedatalab
local$ git remote add dokku dokku@dokku2.ebmdatalab.net:thedatalab
local$ git push dokku master
```

### Use of Dockerfile

[While Dokku normally defaults to using Heroku buildpacks, you can also use \[a\] Dockerfile](http://dokku.viewdocs.io/dokku~v0.21.4/deployment/methods/dockerfiles/)

### Configure environment

Dokku auto-generates `DATABASE_URL`, but the app expects `POSTGRES_*`

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
