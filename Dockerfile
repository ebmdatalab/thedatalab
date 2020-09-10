FROM ubuntu:18.04

ENV LC_CTYPE C.UTF-8
WORKDIR /code/

ADD requirements.txt /code/
RUN apt-get update \
  && apt-get install -y python3 libpython3.6 python3-pip python3-setuptools python3-six python3-idna libpcre3-dev libpq-dev \
  && cat /code/requirements.txt | pip3 --no-cache-dir install -r /dev/stdin \
  && pip3 install uwsgi \
  && apt-get remove -y python3-pip \
  && apt-get autoremove -y \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /code/

ENV DJANGO_SETTINGS_MODULE thedatalab.settings.production

RUN python3 manage.py collectstatic --noinput && python3 manage.py compress

USER www-data
EXPOSE 8000
LABEL io.sitereview.pre-run="./manage.py migrate"
LABEL io.sitereview.pre-link="python3 -c \"import urllib.request; assert urllib.request.urlopen('http://localhost:8000/').code==200\""

# This has to be one long line for dokku compatibility
CMD ["uwsgi --hook-master-start unix_signal:15 gracefully_kill_them_all --http-socket 0.0.0.0:8000 --cheaper 1 --cheaper-algo backlog --workers 8 --master --enable-threads --threads 12 --offload-threads 12 --harakiri 300 --http-harakiri 300 --static-map /media=storage/media --static-map /=webroot --static-expires-uri .* 86400 --static-gzip-all --module thedatalab.wsgi"]
