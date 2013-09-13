from celery import task
from bulkmailer import send_email
#import pdb
#import time
#from django.core.mail import EmailMultiAlternatives

@task.task(ignore_result=True)
def celery_sendmail_task(obj,unsubscribe_url,host,sendopt):
    #time.sleep(10)
    send_email(obj,unsubscribe_url,host,sendopt)
    obj.status=True
    obj.campaign_opt='R'
    obj.save()

'''@task()
def simple_email(sender,subject,html,to_list_unicode):
	#pdb.set_trace()
	time.sleep(10)
	for i in to_list_unicode:
		msg = EmailMultiAlternatives(subject, "", sender, i )
		msg.attach_alternative(html, "text/html")
		msg.send()'''
