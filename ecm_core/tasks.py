from celery import task
from bulkmailer import send_email
from models import CampaignSchedule, SendgridEmailQuota
import redis

import logging
logger = logging.getLogger("ecm_console")


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
	# Lock to ensure task only runs once
	LOCK_EXPIRE = 60 * 30 # Lock expires in 30 minutes
	try:
		obj = CampaignSchedule.objects.get(pk=schedule_id)
		my_lock = redis.Redis().lock(obj.campaign.campaign_uuid,timeout=LOCK_EXPIRE)
		if my_lock.acquire(blocking=False) and obj.campaign.status == False:
			send_email(obj.campaign, obj.unsub_url, obj.ecm_host)
			obj.campaign.status = True
			obj.campaign.save()
			my_lock.release()
		else:
			logger.warn("Task is already running, Lock name:{0} ,Exiting".format(
				obj.campaign.campaign_uuid))
	except Exception, e:
		logger.error("Critical Error : celery_scheduled_campaign: {0} ".format(e))