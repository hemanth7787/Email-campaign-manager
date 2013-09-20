from celery import task
from ecm_sendgridapi.models import  BlocksModel, BouncesModel, UnsubscribesModel, SpamreportsModel, JobstatusModel
import urllib2
import json
from django.utils.encoding import iri_to_uri
import logging
logger = logging.getLogger("ecm_console")
from django.conf import settings
import datetime

from ecm_core.models import Mail_address

@task.task(ignore_result=True)
def ecm_sendgridapi_dbsync():
    job = JobstatusModel.objects.get(purpose="RET_BAD_EMAILS")
    job_status = { "blocks": False, "bounces":False, "unsubscribes": False, "spamreports": False }

    def flag_emal(flag_type,email):
        try:
            contact = Mail_address.objects.get(mail_id__exact=email)
        except Exception, e:
            logger.warn("[ W ]ecm_sengridapi - tasks -- details: {0}".format(e))
            return

        if flag_type == 'spam':
            contact.spam_flag = True
        elif flag_type == 'block':
            contact.block_flag = True
        elif flag_type == 'bounce':
            contact.bounce_flag = True
        elif flag_type == 'unsub':
            contact.unsub_flag = True
        contact.save()

    def update_BlocksModel(job):
        if not job:
            logger.error("Critical Error : JobstatusModel not populated: Periodic tasks wont run;\n Use \"manage.py loaddata jobstatus.json\"")
            return
        apiurl="https://sendgrid.com/api/blocks.get.json?api_user={0}&api_key={1}".format(
            settings.ECM_SENDGRID_USERNAME,
            settings.ECM_SENDGRID_PASSWORD
            )
        encodedurl = iri_to_uri(apiurl)
        try:
            response_data = json.load(urllib2.urlopen(encodedurl)) # This should be a list of dictionaries
            for data in response_data:
                obj, created = BlocksModel.objects.get_or_create(email=data['email'])
                flag_emal('block',data['email'])
            job_status['blocks'] = True
        except Exception, e:
            logger.error("Critical Error : update_BlocksModel: {0} ".format(e))

    def update_BouncesModel(job):
        if not job:
            logger.error("Critical Error : JobstatusModel not populated: Periodic tasks wont run;\n Use \"manage.py loaddata jobstatus.json\"")
            return
        apiurl="https://sendgrid.com/api/bounces.get.json?api_user={0}&api_key={1}".format(
            settings.ECM_SENDGRID_USERNAME,
            settings.ECM_SENDGRID_PASSWORD
            )
        encodedurl = iri_to_uri(apiurl)
        try:
            response_data = json.load(urllib2.urlopen(encodedurl)) # This should be a list of dictionaries
            for data in response_data:
                obj, created = BouncesModel.objects.get_or_create(email=data['email'])
                flag_emal('bounce',data['email'])
            job_status['bounces'] = True
        except Exception, e:
            logger.error("Critical Error : update_BouncesModel: {0} ".format(e))

    def update_UnsubscribesModel(job):
        if not job:
            logger.error("Critical Error : JobstatusModel not populated: Periodic tasks wont run;\n Use \"manage.py loaddata jobstatus.json\"")
            return
        apiurl="https://sendgrid.com/api/unsubscribes.get.json?api_user={0}&api_key={1}".format(
            settings.ECM_SENDGRID_USERNAME,
            settings.ECM_SENDGRID_PASSWORD
            )
        encodedurl = iri_to_uri(apiurl)
        try:
            response_data = json.load(urllib2.urlopen(encodedurl)) # This should be a list of dictionaries
            for data in response_data:
                obj, created = UnsubscribesModel.objects.get_or_create(email=data['email'])
                flag_emal('unsub',data['email'])
            job_status['unsubscribes'] = True
        except Exception, e:
            logger.error("Critical Error : update_UnsubscribesModel: {0} ".format(e))

    def update_SpamreportsModel(job):
        if not job:
            logger.error("Critical Error : JobstatusModel not populated: Periodic tasks wont run;\n Use \"manage.py loaddata jobstatus.json\"")
            return
        apiurl="https://sendgrid.com/api/spamreports.get.json?api_user={0}&api_key={1}".format(
            settings.ECM_SENDGRID_USERNAME,
            settings.ECM_SENDGRID_PASSWORD,
            )
        encodedurl = iri_to_uri(apiurl)
        try:
            response_data = json.load(urllib2.urlopen(encodedurl)) # This should be a list of dictionaries
            for data in response_data:
                obj, created = SpamreportsModel.objects.get_or_create(email=data['email'])
                flag_emal('spam',data['email'])
            job_status['spamreports'] = True
        except Exception, e:
            logger.error("Critical Error : update_SpamreportsModel: {0} ".format(e))

    update_BlocksModel(job)
    update_BouncesModel(job)
    update_UnsubscribesModel(job)
    update_SpamreportsModel(job)
    if job_status['blocks'] and job_status['bounces'] and job_status['unsubscribes'] and job_status['spamreports']:
        job.lastrun  = datetime.date.today() - datetime.timedelta(days=1) 
        # saving Yesterday's date because of timezone diffrences between our server and sendgrid so a - 24 hr is safe
        job.save()
        logger.info("Success : update job  ")
    else:
        logger.error("Warning : update job: {0}".format(job_status))


