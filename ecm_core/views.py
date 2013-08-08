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

from tasks import celery_add_task


@login_required(login_url='/login')
@csrf_protect
def Import_csv(request):
	'''def handle_uploaded_file(f,cid):
		return #TODO handle the fun here
		with open('/tmp/'+f.name, 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
		csv_to_db(f,cid)'''

	iform=Importform
	if request.method == "POST":
		iform=Importform(request.POST,request.FILES)
		if iform.is_valid():
			cid = request.POST['cat_drop']
			csv_file = iform.cleaned_data.get('csv_file')
			#TODO handle_uploaded_file(csv_file,cid)
			parse_csv(csv_file,cid,ignore_errors=True)
			status="updated"
			messages.success(request,"CSV file imported successfully")
			
	return render(request,'import_csv.html',{'iform':iform ,})


@login_required(login_url='/login')
@csrf_protect
def campain(request):
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
			#send_email(obj)
			celery_add_task.delay(obj)
			messages.success(request,"Run campain successfull")
	return render(request, "run_campain.html",{'cform':cform ,})


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
	

