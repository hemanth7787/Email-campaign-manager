##copy PIL
manage.py loaddata jobstatus.json
manage.py celery worker -B

Pillow is dependency make sure to install libs on server


sudo apt-get install python-dev python-setuptools libjpeg62-dev zlib1g-dev libfreetype6-dev

