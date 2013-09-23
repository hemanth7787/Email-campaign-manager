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
from django.core.mail import EmailMultiAlternatives
import pdb

import SmtpApiHeader #local file
import json
from ecm_track.TrackHelper import TrackCode

def send_email(obj,unsubscribe_url,host,sendopt):
    for mlist in obj.mailing_list.all():
        if sendopt == 'N':
            to_list = Mail_address.objects.filter(mail_list=mlist)
        else: # Q
            to_list = Mail_address.objects.filter(mail_list=mlist).exclude(spam_flag=True).exclude(unsub_flag=True).exclude(block_flag=True).exclude(bounce_flag=True)
        tracked_email(obj,to_list,unsubscribe_url,host)

def tracked_email(campaign_obj,mail_addr_obj,unsubscribe_url,host):
    subj = str(campaign_obj.subject)
    html = str(campaign_obj.html)
    if campaign_obj.sender_name:
        sender = "{0} <{1}>".format(campaign_obj.sender_name,campaign_obj.sender)
    else:
        sender = str(campaign_obj.sender)
    uuid = str(campaign_obj.campaign_uuid)
    hdr = SmtpApiHeader.SmtpApiHeader()
    hdr.setCategory(str(campaign_obj.category()))
    #API https://sendgrid.com/api/stats.get.json?api_user=username&api_key=password&list=true&category=category
    for mobj in mail_addr_obj:
        if mobj.subscribed:
            uslink=unsubscribe_url+mobj.uid+"/"
            #uslink_append="If you would like to unsubscribe and stop receiving these emails <a href=\"{0}\" target=\"_blank\">click here</a>".format(uslink)
            try:
                mail_body = html.format(unsubscribe=uslink)
            except:
                mail_body = html
            track_code= TrackCode(host,mobj,uuid)
            mail_body+=track_code
            msg = EmailMultiAlternatives(subj, "", sender, [mobj.mail_id], headers={"X-SMTPAPI": hdr.asJSON()})
            msg.attach_alternative(mail_body, "text/html")
            msg.send()

def check_email(email, ignore_errors=False):
    if settings.DEBUG:
        logger.debug("Checking e-mail address %s", email)

    email_length = Mail_address._meta.get_field_by_name('mail_id')[0].max_length

    if len(email) <= email_length or ignore_errors:
        return email[:email_length]
    else:
        raise forms.ValidationError(_(
            "E-mail address %(email)s too long, maximum length is "
            "%(email_length)s characters.") % {
                "email": email,
                "email_length": email_length})

def vlen(data, length):
    # VALIDATE LENGTH   
    if len(data) <= length:
        return data[:length]
    else:
        return data[:length-1]+">"

def add_contact(mailinglist, contact):
    con = Mail_address()
    con.mail_id     = contact['email']
    con.First_Name  = contact['first_name']
    con.Last_Name   = contact['last_name']
    con.Middle_Name = contact['mid_name']
    if contact['dob']:
        con.Date_of_Birth = contact['dob']
    con.Gender  = contact['gender']
    con.Country = contact['country']
    con.City    = contact['city']
    con.Direct_Phone  = contact['direct_phone']
    con.Mobile      = contact['mobile']
    con.Address_1   = contact['Address_1']
    con.Address_2   = contact['Address_2']
    con.Zip = contact['zipcode']
    con.Telephone_1 = contact['telephone_1']
    con.Telephone_2 = contact['telephone_2']
    con.Company   = contact['company']
    con.Job_Title = contact['job_title']
    con.Website   = contact['website']
    con.mail_list_id = mailinglist
    con.subscribed = True
    con.save()

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
    first_namecol = None
    for column in firstrow:
        if "first name" in column.lower() or ugettext("first name") in column.lower():
            first_namecol = colnum
            break # First Name as name

            if "display" in column.lower() or \
                    ugettext("display") in column.lower():
                break

        colnum += 1

    if first_namecol is None:
        raise forms.ValidationError(_(
            "Name column not found. The name of this column should be "
            "either 'first name' or '%s'.") % ugettext("first name"))

    logger.debug("Name column found: '%s'", firstrow[first_namecol])

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

    colnum = 0
    last_namecol = None
    for column in firstrow:
        if "last name" in column.lower() or ugettext("last name") in column.lower():
            last_namecol = colnum
            break

        colnum += 1

    colnum = 0
    mid_namecol = None
    for column in firstrow:
        if "middle name" in column.lower() or ugettext("middle name") in column.lower():
            mid_namecol = colnum
            break

        colnum += 1

    colnum = 0
    dob_col = None
    for column in firstrow:
        if "date of birth" in column.lower() or ugettext("date of birth") in column.lower():
            dob_col = colnum
            break

        colnum += 1

    colnum = 0
    gen_col = None
    for column in firstrow:
        if "gender" in column.lower() or ugettext("gender") in column.lower():
            gen_col = colnum
            break

        colnum += 1

    colnum = 0
    country_col = None
    for column in firstrow:
        if "country" in column.lower() or ugettext("country") in column.lower():
            country_col = colnum
            break

        colnum += 1

    colnum = 0
    city_col = None
    for column in firstrow:
        if "city" in column.lower() or ugettext("city") in column.lower():
            city_col = colnum
            break

        colnum += 1

    colnum = 0
    direct_phone_col = None
    for column in firstrow:
        if "direct phone" in column.lower() or ugettext("direct phone") in column.lower():
            direct_phone_col = colnum
            break

        colnum += 1


    colnum = 0
    mobile_col = None
    for column in firstrow:
        if "mobile" in column.lower() or ugettext("mobile") in column.lower():
            mobile_col = colnum
            break

        colnum += 1

    colnum = 0
    Address_1_col = None
    for column in firstrow:
        if "address 1" in column.lower() or ugettext("address 1") in column.lower():
            Address_1_col = colnum
            break

        colnum += 1

    colnum = 0
    Address_2_col = None
    for column in firstrow:
        if "address 2" in column.lower() or ugettext("address 2") in column.lower():
            Address_2_col = colnum
            break

        colnum += 1

    colnum = 0
    zip_col = None
    for column in firstrow:
        if "zip" in column.lower() or ugettext("zip") in column.lower():
            zip_col = colnum
            break

        colnum += 1

    colnum = 0
    telephone_1_col = None
    for column in firstrow:
        if "telephone 1" in column.lower() or ugettext("telephone 1") in column.lower():
            telephone_1_col = colnum
            break

        colnum += 1

    colnum = 0
    telephone_2_col = None
    for column in firstrow:
        if "telephone 2" in column.lower() or ugettext("telephone 2") in column.lower():
            telephone_2_col = colnum
            break

        colnum += 1

    colnum = 0
    company_col = None
    for column in firstrow:
        if "company" in column.lower() or ugettext("company") in column.lower():
            company_col = colnum
            break

        colnum += 1

    colnum = 0
    job_title_col = None
    for column in firstrow:
        if "job title" in column.lower() or ugettext("job title") in column.lower():
            job_title_col = colnum
            break

        colnum += 1

    colnum = 0
    website_col = None
    for column in firstrow:
        if "website" in column.lower() or ugettext("website") in column.lower():
            website_col = colnum
            break

        colnum += 1

    #assert namecol != mailcol, \
    #    'Name and e-mail column should not be the same.'
    if first_namecol == mailcol:
        raise forms.ValidationError(_(
            "Could not properly determine the proper columns in the "
            "CSV-file. There should be a field called 'name' or '%(name)s' "
            "and one called 'e-mail' or '%(e-mail)s'.") % {
                "name": _("name"),
                "e-mail": _("e-mail")})

    logger.debug('Extracting data.')

    addresses = {}
    for row in myreader:
        if not max(first_namecol, mailcol) < len(row):
            logger.warn("Column count does not match for row number %d",
                        myreader.line_num, extra=dict(data={'row': row}))

            if ignore_errors:
                # Skip this record
                continue
            else:
                raise forms.ValidationError(_(
                    "Row with content '%(row)s' does not contain a name and "
                    "email field.") % {'row': row})

        contact = dict()
        contact['email']      = check_email(row[mailcol], ignore_errors)
        contact['first_name'] = vlen(row[first_namecol],100)
        contact['last_name']  = vlen(row[last_namecol],100)
        contact['mid_name']   = vlen(row[mid_namecol],100)
        contact['dob']        = row[dob_col]
        contact['gender']     = vlen(row[gen_col],5)
        contact['country']    = vlen(row[country_col],100)
        contact['city']       = vlen(row[city_col],100)
        contact['direct_phone'] = vlen(row[direct_phone_col],20)
        contact['mobile']       = vlen(row[mobile_col],15)
        contact['Address_1']    = row[Address_1_col]
        contact['Address_2']    = row[Address_2_col]
        contact['zipcode']      = vlen(row[zip_col],15)
        contact['telephone_1']  = vlen(row[telephone_1_col],15)
        contact['telephone_2']  = vlen(row[telephone_2_col],15)
        contact['company']      = vlen(row[company_col],100)
        contact['job_title']    = vlen(row[job_title_col],100)
        contact['website']      = vlen(row[website_col],100)


        '''email,first_name, last_name, mid_name, dob, gender,
        country, city, direct_phone, mobile, Address_1,
        Address_2, zipcode, telephone_1,telephone_2,
        company, job_title, website'''

        count+=1
        logger.debug("Going to add %s <%s> %d", contact['first_name'], contact['email'], count)

        if email_re.search(contact['email']):
            add_contact(mlist,contact)
        elif not ignore_errors:
                raise forms.ValidationError(_(
                    "Entry '%s' does not contain a valid "
                    "e-mail address.") % contact['first_name'])
        else:
            logger.warn(
                "Entry '%s' at line %d does not contain a valid "
                "e-mail address.",
                contact['first_name'], myreader.line_num, extra=dict(data={'row': row}))
