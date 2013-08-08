import SmtpApiHeader
import json
from django.core.mail import EmailMultiAlternatives
#import pdb
#from celery import task

def burst_email(sender,subject,html,to_list_unicode):
    hdr = SmtpApiHeader.SmtpApiHeader()
    hdr.addTo(to_list_unicode)

    # Specify that this is an initial contact message
    #hdr.setCategory("initial")
    # Enable a text footer and set it
    #hdr.addFilterSetting('footer', 'enable', 1)
    #hdr.addFilterSetting('footer', "text/plain", "If you dont wish to receive Emails from us ,Unsubscribe here talentcall.com/accounts/profile/#id_is_emails_fine")

    msg = EmailMultiAlternatives(subject, "", sender, [sender], headers={"X-SMTPAPI": hdr.asJSON()})
    msg.attach_alternative(html, "text/html")
    msg.send()

#@task() 
def simple_email(sender,subject,html,to_list_unicode):
	#pdb.set_trace()
	for i in to_list_unicode:
		msg = EmailMultiAlternatives(subject, "", sender, i )
		msg.attach_alternative(html, "text/html")
		msg.send()
