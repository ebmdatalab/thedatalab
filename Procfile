release: python3 manage.py migrate && python3 manage.py collectstatic --noinput && python3 manage.py compress
web: gunicorn --bind 0.0.0.0:8000 thedatalab.wsgi
