##copy PIL
manage.py loaddata jobstatus.json
manage.py celery worker -B
