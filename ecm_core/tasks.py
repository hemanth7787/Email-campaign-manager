from celery import task
from bulkmailer import send_email
from models import CampaignSchedule, SendgridEmailQuota
import logging
logger = logging.getLogger("ecm_console")
#import pdb
#import time
#from django.core.mail import EmailMultiAlternatives

@task.task(ignore_result=True)
def celery_sendmail_task(obj,unsubscribe_url,host):
    #time.sleep(10)
    send_email(obj,unsubscribe_url,host)
    obj.status=True
    if obj.campaign_opt=='S':
    	obj.campaign_opt='R'
    obj.save()

@task.task(ignore_result=True)
def sendgrid_quota_reset():
	try:
		quota = SendgridEmailQuota.objects.get(pk=1)
		quota.used=0
		quota.save()
		logger.info("Success : sendgrid_quota_reset job ")
	except Exception, e:
		logger.error("Critical Error : sendgrid_quota_reset: {0} ".format(e))

@task.task(ignore_result=True)
def celery_scheduled_campaign(schedule_id):
	try:
		obj = CampaignSchedule.objects.get(pk=schedule_id)
		send_email(obj.campaign, obj.unsub_url, obj.ecm_host)
		obj.campaign.status = True
		obj.campaign.save()
	except Exception, e:
		logger.error("Critical Error : celery_scheduled_campaign: {0} ".format(e))