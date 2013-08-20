from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from forms import Importform ,ListBasketForm ,mailtemplateform #,campainform,addcform
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from models import Mail_address, Mailing_list, campaign as modelcampaign, mailtemplate
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
from django.core.urlresolvers import get_script_prefix
import pdb
import os



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
    camps = modelcampaign.objects.filter(status = True)
    #pdb.set_trace()
    return render(request, "campain_report.html",{'camps':camps,})

def dummy_login_redirect(request):
    return HttpResponse(json.dumps({'status':'login_err'}), content_type="application/json")

@login_required(login_url=get_script_prefix() + "ecm/dummy/login_redirect")
@csrf_protect
def json_report(request):
    response_data = dict()
    try:
        category=request.POST['category']
    except:
        response_data['status'] = 'data_err'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    urlappend="&category="+category
    apiurl="https://sendgrid.com/api/stats.get.json?api_user={0}&api_key={1}&aggregate=1".format(settings.ECM_SENDGRID_USERNAME,settings.ECM_SENDGRID_PASSWORD)
    apiurl+=urlappend
    encodedurl = iri_to_uri(apiurl)
    #logger.info(" Details :  {0} ".format(encodedurl))
    try:
        response_data = json.load(urllib2.urlopen(encodedurl))[0] # This should be a dict
        response_data[unicode('status')] = unicode("success")
    except urllib2.HTTPError, e:
        logger.error("Campaign repot Error | Details :  {0} ".format(e))
        response_data['status'] = "failed"
    #pdb.set_trace()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url='/login')
@csrf_protect
def campaign(request):
	return render(request, "campaign.html")

def view_campaign(request):
	camps = modelcampaign.objects.all()
	return render(request, "view_campaign.html",{'camps':camps})

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

from bs4 import BeautifulSoup
from zipfile import ZipFile
def templates_new(request):
	def adapt_template(path,obj,request):
		fp = open(path+'/index.html','r')
		original_html = fp.read()
		soup  = BeautifulSoup(original_html)
		asseturl = request.META['HTTP_ORIGIN']+"/"+path+"images"
		for link in soup.find_all('img'):
			link['src']=link['src'].replace("images",asseturl)
		obj.html=str(soup)
		obj.save()
		#pdb.set_trace()
	def process_zip(obj,request):
		path=str("media/extracted/"+obj.uuid+"/")
		with ZipFile(obj.zipfile, 'r') as myzip:
			myzip.extractall(path)
			adapt_template(path,obj,request)
	form=mailtemplateform
	if request.method == "POST":
		form=mailtemplateform(request.POST,request.FILES)
		if form.is_valid():
			#cid = request.POST['cat_id']
			#send_id = request.POST['email_id']
			#send_id='noreply@orange-mailer.net'
			#subj = request.POST['subj']
			obj = form.save()
			process_zip(obj,request)
			messages.success(request,"Email template saved successfully")
	return render(request, "templates_new.html",{'form':form})

def templates_view(request):
	qset = mailtemplate.objects.all()
	return render(request, "templates_view.html",{'mailtemplate':qset})

def templates_preview(request,usid):
	if not usid=='nill':
		try:
			temp=mailtemplate.objects.get(id=usid)
			htm = temp.html
		except Exception, e:
			#logger.error(" Details :  {0} ".format(e))
			return HttpResponse("<h2>Error : Not a valid template .. !</h2>", content_type="text/html")
	return HttpResponse(htm, content_type="text/html")

def templates_delete(request,usid):
	if not usid=='nill':
		try:
			temp=mailtemplate.objects.get(id=usid)
			temp.delete()
		except Exception, e:
			#logger.error(" Details :  {0} ".format(e))
			return HttpResponse("<h2>Error : Could not delete .. !</h2>", content_type="text/html")
	return redirect("/ecm/templates-view/")












@csrf_protect
def login(request):
	pagename='login'
	authentication_form=AuthenticationForm
	if request.method == "POST":
		form = authentication_form(data=request.POST)
		if form.is_valid():
			auth_login(request, form.get_user())
			if request.session.test_cookie_worked():
				request.session.delete_test_cookie()
			context = {
				'user': request.user,
				}
			messages.info(request,"Welcome "+request.user.username+" .")
			return HttpResponseRedirect('/')
	else:
		form = authentication_form(request)
	context = {
			'form': form,
			'pagename':pagename
			}
	return render(request, 'registration/login.html', context)


def logout(request):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    pagename='logout'
    auth_logout(request)
    return render(request, 'registration/logout.html',{'pagename':pagename})
#-------------------------------------------------------------------------------------

'''@login_required(login_url='/login')
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
		
	return redirect('/category')'''
	

