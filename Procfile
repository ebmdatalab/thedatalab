release: python3 manage.py migrate && python3 manage.py collectstatic --noinput && python3 manage.py compress
web: uwsgi --hook-master-start unix_signal:15 gracefully_kill_them_all \
  --http-socket 0.0.0.0:8000 \
  --workers 3 \
  --master \
  --enable-threads \
  --threads 12 \
  --offload-threads 12 \
  --harakiri 300 \
  --http-harakiri 300 \
  --static-map /media=storage/media \
  --static-map /=webroot \
  --static-expires-uri .* 86400 \
  --static-gzip-all \
  --module thedatalab.wsgi
