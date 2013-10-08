##copy PIL
manage.py loaddata jobstatus.json
manage.py celery worker -B

Pillow is dependency make sure to install libs on server


sudo apt-get install python-dev python-setuptools libjpeg62-dev zlib1g-dev libfreetype6-dev


[ Running under Apache + mod_wsgi ]-------------------
1.modify pro_settings.py , index.wsgi, and config/etc-apache2../myvhost according to your project and directory structure
2.copy myvhost to /etc/apache/sites-avalaible
3.add a2ensite myvhost
4.sudo service apache2 reload
5.sudo service apache2 restart
 
