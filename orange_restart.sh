#!/bin/bash
ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
ps auxww | grep 'manage.py' | awk '{print $2}' | xargs kill -9
source /home/hemanth/working_ecm/env/bin/activate
nohup python manage.py celery worker -B --settings=email_campaign_manager.local_settings --loglevel=info > celery.log &
nohup python manage.py runserver codestager.com:8060 --settings=email_campaign_manager.local_settings > django.log &

