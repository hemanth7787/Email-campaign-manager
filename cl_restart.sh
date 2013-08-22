#!/bin/bash
ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
ps auxww | grep 'manage.py' | awk '{print $2}' | xargs kill -9
source env/bin/activate
nohup python manage.py celery worker --settings=email_campaign_manager.local_settings --loglevel=info > celery.log &
nohup python manage.py runserver codestager.com:8050 --settings=email_campaign_manager.local_settings > django.log &

