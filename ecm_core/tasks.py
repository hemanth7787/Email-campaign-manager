from celery import task
from bulkmailer import send_email
from models import SendgridEmailQuota
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
