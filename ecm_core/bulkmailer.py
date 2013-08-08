from django.core.mail import send_mail,EmailMultiAlternatives
from models import Mail_address, Mailing_list, campaign

#Parsecsv
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
import pdb
import logging
#logger = logging.getLogger(__name__)
#TODO Below is a dbug line, change that to log file
logger = logging.getLogger("ecm_console")
from django import forms
from django.conf import settings
from django.core.validators import email_re
from models import Mail_address
#import pdb

from ecm_sengrid_xsmtpapi import simple_email

def send_email(obj):
	#pdb.set_trace()
	subj=str(obj.subject)
	html=str(obj.html)
	sender = str(obj.sender)
	for mlist in obj.mailing_list.all():
		#logger.info(Mail_address.objects.filter(mail_list=mlist).values_list('mail_id',flat=True))
		to_list = Mail_address.objects.filter(mail_list=mlist).values_list('mail_id')
		simple_email(sender,subj,html,to_list)


'''def explode_mail(f,cid,sid,subject):
	template=f.read()
	
	#TODO: Remove below hardcoded sender email and use from_email=str(sid)
	from_email='noreply@orange-mailer.net'
	text_content = ''
	#Repto='Reply-To: hemanth7787@gmail.com'
	html_content = template
	inbox_list=Mail_address.objects.filter(cid=cid)
	for target_inbox in inbox_list:
		to = str(target_inbox.mid)
		msg = EmailMultiAlternatives(subject, text_content, from_email,[to])
		#msg.headers= {'reply-to','hemanth@success.com'}
		msg.attach_alternative(html_content, "text/html")	
		msg.send()'''

def check_email(email, ignore_errors=False):
    if settings.DEBUG:
        logger.debug("Checking e-mail address %s", email)

    email_length = 30 #\
        #Subscription._meta.get_field_by_name('email_field')[0].max_length

    if len(email) <= email_length or ignore_errors:
        return email[:email_length]
    else:
        raise forms.ValidationError(_(
            "E-mail address %(email)s too long, maximum length is "
            "%(email_length)s characters.") % {
                "email": email,
                "email_length": email_length})

def check_name(name, ignore_errors=False):
    if settings.DEBUG:
        logger.debug("Checking name: %s", name)

    #TODO V name_length = \
    #    Subscription._meta.get_field_by_name('name_field')[0].max_length
    name_length=30    
    if len(name) <= name_length or ignore_errors:
        return name[:name_length]
    else:
        raise forms.ValidationError(_(
            "Name %(name)s too long, maximum length is "
            "%(name_length)s characters.") % {
                "name": name,
                "name_length": name_length})

def add_contact(mailinglist, email, cname=None):
    Mail_address(
                 name = cname,
                 mail_list_id = mailinglist,
                 subscribed = True,
                 mail_id = email,
                 ).save()

def parse_csv(myfile, mlist, ignore_errors=False):
    from ecm_core.addressimport.csv_util import UnicodeReader
    import codecs
    import csv
    count = 0 
    # Detect encoding
    from chardet.universaldetector import UniversalDetector

    detector = UniversalDetector()

    for line in myfile.readlines():
        detector.feed(line)
        if detector.done:
            break

    detector.close()
    charset = detector.result['encoding']

    # Reset the file index
    myfile.seek(0)

    # Attempt to detect the dialect
    encodedfile = codecs.EncodedFile(myfile, charset)
    dialect = csv.Sniffer().sniff(encodedfile.read(1024))

    # Reset the file index
    myfile.seek(0)

    logger.info('Detected encoding %s and dialect %s for CSV file',
                charset, dialect)

    myreader = UnicodeReader(myfile, dialect=dialect, encoding=charset)

    firstrow = myreader.next()

    # Find name column
    colnum = 0
    namecol = None
    for column in firstrow:
        if "name" in column.lower() or ugettext("name") in column.lower():
            namecol = colnum
            break # First Name as name

            if "display" in column.lower() or \
                    ugettext("display") in column.lower():
                break

        colnum += 1

    if namecol is None:
        raise forms.ValidationError(_(
            "Name column not found. The name of this column should be "
            "either 'name' or '%s'.") % ugettext("name"))

    logger.debug("Name column found: '%s'", firstrow[namecol])

    # Find email column
    colnum = 0
    mailcol = None
    for column in firstrow:
        if 'email' in column.lower() or \
                'e-mail' in column.lower() or \
                ugettext("e-mail") in column.lower():

            mailcol = colnum

            break

        colnum += 1

    if mailcol is None:
        raise forms.ValidationError(_(
            "E-mail column not found. The name of this column should be "
            "either 'email', 'e-mail' or '%(email)s'.") %
            {'email': ugettext("e-mail")})

    logger.debug("E-mail column found: '%s'", firstrow[mailcol])

    #assert namecol != mailcol, \
    #    'Name and e-mail column should not be the same.'
    if namecol == mailcol:
        raise forms.ValidationError(_(
            "Could not properly determine the proper columns in the "
            "CSV-file. There should be a field called 'name' or '%(name)s' "
            "and one called 'e-mail' or '%(e-mail)s'.") % {
                "name": _("name"),
                "e-mail": _("e-mail")})

    logger.debug('Extracting data.')

    addresses = {}
    for row in myreader:
        if not max(namecol, mailcol) < len(row):
            logger.warn("Column count does not match for row number %d",
                        myreader.line_num, extra=dict(data={'row': row}))

            if ignore_errors:
                # Skip this record
                continue
            else:
                raise forms.ValidationError(_(
                    "Row with content '%(row)s' does not contain a name and "
                    "email field.") % {'row': row})

        name = check_name(row[namecol], ignore_errors)
        email = check_email(row[mailcol], ignore_errors)

        count+=1
        logger.debug("Going to add %s <%s> %d", name, email,count)

        if email_re.search(email):
            #TODO addr = make_subscription(newsletter, email, name)
            #pdb.set_trace()
            add_contact(mlist,email,name)
        elif not ignore_errors:
                raise forms.ValidationError(_(
                    "Entry '%s' does not contain a valid "
                    "e-mail address.") % name)
        else:
            logger.warn(
                "Entry '%s' at line %d does not contain a valid "
                "e-mail address.",
                name, myreader.line_num, extra=dict(data={'row': row}))

        '''if addr:
            if email in addresses:
                logger.warn(
                    "Entry '%s' at line %d contains a "
                    "duplicate entry for '%s'",
                    name, myreader.line_num, email,
                    extra=dict(data={'row': row}))

                if not ignore_errors:
                    raise forms.ValidationError(_(
                        "The address file contains duplicate entries "
                        "for '%s'.") % email)

            addresses.update({email: addr})
        else:
            logger.warn(
                "Entry '%s' at line %d is already subscribed to "
                "with email '%s'",
                name, myreader.line_num, email, extra=dict(data={'row': row}))

            if not ignore_errors:
                raise forms.ValidationError(
                    _("Some entries are already subscribed to."))

    return addresses'''

