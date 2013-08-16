from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from forms import Importform ,ListBasketForm #,campainform,addcform
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from models import Mail_address, Mailing_list, campaign
#from loaddata import csv_to_db
from bulkmailer import parse_csv, send_email

from tasks import celery_sendmail_task

from django.http import HttpResponse
from django.conf import settings

import urllib2
import json
from django.utils.encoding import iri_to_uri
#TODO
import logging
logger = logging.getLogger("ecm_console")

from django.db.models import Count


@login_required(login_url='/login')
@csrf_protect
def import_csv(request):
	iform=Importform
	if request.method == "POST":
		iform=Importform(request.POST,request.FILES)
		if iform.is_valid():
			
			name = request.POST['name']
			#cid = request.POST['mailing_list']
			mlist = Mailing_list(title = name)
			mlist.save()
			csv_file = iform.cleaned_data.get('csv_file')
			#TODO handle_uploaded_file(csv_file,cid)
			parse_csv(csv_file,mlist.id,ignore_errors=True)
			status="updated"
			messages.success(request,"Contacts imported successfully")
			
	return render(request,'import_csv.html',{'iform':iform ,})


@login_required(login_url='/login')
@csrf_protect
def run_campaign(request):
	cform=ListBasketForm
	if request.method == "POST":
		cform=ListBasketForm(request.POST,request.FILES)
		if cform.is_valid():
			#cid = request.POST['cat_id']
			#send_id = request.POST['email_id']
			#send_id='noreply@orange-mailer.net'
			#subj = request.POST['subj']
			#explode_mail(request.FILES['t_file'],cid,send_id,subj)
			obj = cform.save()
			unsubscribe_url=request.build_absolute_uri()+"unsubscribe/"
			#send_email(obj,unsubscribe_url)
			celery_sendmail_task.delay(obj,unsubscribe_url)
			messages.success(request,"Run campain successfull")
	return render(request, "run_campain.html",{'cform':cform ,})

def unsubscribe(request,usid):
	if not usid=='nill':
		try:
			contact=Mail_address.objects.get(uid=usid)
			contact.subscribed=False
			contact.save()
		except:
			pass
	return HttpResponse("<h2>You have successfully unsubscribed from our mailing list.</h2>", content_type="text/html")

@login_required(login_url='/login')
@csrf_protect
def campaign_report(request):
	urlappend=""
	for obj in campaign.objects.filter(status=True):
		urlappend+="&category[]="+obj.subject+"-"+obj.campaign_uuid
	apiurl="https://sendgrid.com/api/stats.get.json?api_user={0}&api_key={1}".format(settings.ECM_SENDGRID_USERNAME,settings.ECM_SENDGRID_PASSWORD)
	apiurl+=urlappend
	#raise NameError(apiurl)
	encodedurl = iri_to_uri(apiurl)
	try:
		see = json.load(urllib2.urlopen(encodedurl)) # pls handle invalid reqs
	except urllib2.HTTPError, e:
		logger.error("Campaign repot Error | Details :  {0}".format(e))
		see={}
	return render(request, "campain_report.html",{'see':see,})

@login_required(login_url='/login')
@csrf_protect
def campaign(request):
	return render(request, "campaign.html")

def test(request):
	messages.success(request,"This is so awesome !!!!!!! ")
	return render(request, "test.html")

def contacts(request):
	return render(request, "contacts.html")

def contacts_view(request):
	maddr = Mail_address.objects.all()
	return render(request, "contacts_view.html",{'contacts':maddr})


def contacts_statistics(request):
	mlist = Mailing_list.objects.annotate(addrcount=Count('mail_address'))
	return render(request, "contact_statistics.html",{'mailing_list':mlist})

def templates(request):
	return render(request, "templates.html")

def home(request):
	return render(request, "home.html")

#-------------------------------------------------------------------------------------

@login_required(login_url='/login')
@csrf_protect
def run_campain(request):
	categories=Categories.objects.all()
	cform=campainform
	status="notset"
	if request.method == "POST":
		cform=campainform(request.POST,request.FILES)
		if cform.is_valid():
			cid = request.POST['cat_id']
			#send_id = request.POST['email_id']
			send_id='noreply@orange-mailer.net'
			subj = request.POST['subj']
			explode_mail(request.FILES['t_file'],cid,send_id,subj)
			status="updated"
			messages.success(request,"Run campain successfull")
	return render(request, "run_campain.html",{'cform':cform ,'categories':categories, 'status' : status})

def home(request):
	return render(request, "home.html")

@login_required(login_url='/login')
@csrf_protect
def category(request):
	add_cat_form=addcform
	status="notset"
	categories=Categories.objects.all()
	return render(request, "category.html",{'status':status,'categories':categories,'add_cat_form':add_cat_form})

@login_required(login_url='/login')
@csrf_protect
def delete_cat(request):
	status="notset"
	if request.method == "POST":
		to_delete = request.POST['del_id']
		cats=Categories.objects.get(id=to_delete)
		cats.delete()
		status='deleted'
		messages.warning(request,"Successfully Deleted")
	return redirect('/category')

@login_required(login_url='/login')
@csrf_protect
def add_cat(request):
	status="notset"
	if request.method == "POST":
		to_add = request.POST['cat_name']
		boll=Categories.objects.filter(cname=to_add).exists()
		if boll:
			messages.error(request,"Error - Category already exists")
		else:		
			cats=Categories()
			cats.cname=to_add
			cats.save()
			status='saved'
			messages.success(request,"Successfully saved")
		
	return redirect('/category')
	

