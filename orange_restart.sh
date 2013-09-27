#!/bin/bash
source /home/hemanth/working_ecm/env/bin/activate
nohup python manage.py celery worker -B --settings=email_campaign_manager.local_settings --loglevel=info --concurrency=1 > celery.log &
nohup python manage.py runserver codestager.com:8060 --settings=email_campaign_manager.local_settings > django.log &

