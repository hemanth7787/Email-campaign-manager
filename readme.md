##copy PIL
manage.py loaddata jobstatus.json
python manage.py loaddata sendgridquota.json
manage.py celery worker -B

Pillow is dependency make sure to install libs on server

install redis server

sudo apt-get install python-dev python-setuptools libjpeg62-dev zlib1g-dev libfreetype6-dev redis-server python-virtualenv build-essential


[ Running under Apache + mod_wsgi ]-------------------
1.modify pro_settings.py , index.wsgi, and config/etc-apache2../myvhost according to your project and directory structure
2.copy myvhost to /etc/apache/sites-avalaible
3.add a2ensite myvhost
4.sudo service apache2 reload
5.sudo service apache2 restart
 

sudo apt-get install libapache2-mod-wsgi
sudo a2enmod wsgi

sudo apt-get install redis-server


index.wsgi not used

python-virtualenv
build-essential


/var/log/celery-ecm.log
/home/vikas/ecm/error.log

sudo apt-get install python-virtualenv  build-essential
cd /home/vikas/ecm
rm -r env/
virtualenv env
source env/bin/activate
pip install -r requirements2.txt


