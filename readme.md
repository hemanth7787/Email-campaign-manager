# ECM

An online email marketing solution in [Django] using [Sendgrid] mail service. [currently unmaintianed]

#### OS Setup(ubuntu):

```sh
sudo apt-get build-dep python-imaging
sudo apt-get install redis-server python-virtualenv
git clone https://github.com/hemanth7787/Email-campaign-manager.git ecm && cd ecm
virtualenv env && source env/bin/activate
pip install -r requirements.txt
pip install https://github.com/hemanth7787/django-cked-1/archive/master.zip
```
#### App setup:
```sh
python manage.py loaddata jobstatus.json
python manage.py loaddata sendgridquota.json
manage.py celery worker -B #(required for backround tasks and sending emails)
```



#### Running under Apache + mod_wsgi 

- Modify pro_settings.py , index.wsgi, and config/etc-apache2/myvhost according to your project and directory structure.
- Copy myvhost to /etc/apache/sites-avalaible
- ```sudo apt-get install libapache2-mod-wsgi && sudo a2enmod wsgi```
- ```sudo a2ensite myvhost && sudo service apache2 reload && sudo service apache2 restart```

[Sendgrid]: <https://sendgrid.com/>
[Django]: <https://www.djangoproject.com/>
