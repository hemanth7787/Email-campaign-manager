from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from forms import Importform ,ListBasketForm ,mailtemplateform, cleanupform
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

from django.db.models import Count, Q
from django.core.urlresolvers import get_script_prefix
import pdb
import os
from bs4 import BeautifulSoup
from zipfile import ZipFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ecm_sendgridapi.models import BlocksModel, BouncesModel, UnsubscribesModel, SpamreportsModel



@login_required(login_url='/login')
@csrf_protect
def import_csv(request):
    iform=Importform
    if request.method == "POST":
        iform=Importform(request.POST,request.FILES)
        if iform.is_valid():
            try:
                name = request.POST['name']
                mlist = Mailing_list(title = name)
                mlist.save()
                csv_file = iform.cleaned_data.get('csv_file')
                parse_csv(csv_file,mlist.id,ignore_errors=True)
                status="updated"
                messages.success(request,"Contacts imported successfully")
            except Exception, e:
                logger.error("Import CSV Error | Details :  {0} ".format(e))
                messages.error(request,"Import failed, wrong CSV format..! ")

    return render(request,'import_csv.html',{'iform':iform ,})


@login_required(login_url='/login')
@csrf_protect
def run_campaign(request):
    cform=ListBasketForm
    if request.method == "POST":
        cform=ListBasketForm(request.POST,request.FILES)
        if cform.is_valid():
            content_type = request.POST['content_type']
            pro_campaign = cform.save(commit=False)
            if content_type == 'P':
                pass
            elif content_type == 'T':
                try:
                    temp=mailtemplate.objects.get(id=request.POST['template'])
                    pro_campaign.html=temp.html
                except:
                    messages.error(request,"Please choose a template, or create a new one before submitting campaigns")
                    return render(request, "run_campain.html",{'cform':cform ,})
            elif content_type == 'W':
                pass
            pro_campaign.save()
            cform.save_m2m()  # PITFALL
            #pdb.set_trace()
            unsubscribe_url=request.build_absolute_uri()+"unsubscribe/"
            ecm_host = request.META['HTTP_ORIGIN']
            #pdb.set_trace()
            #send_email(pro_campaign,unsubscribe_url,ecm_host)
            celery_sendmail_task.delay(pro_campaign,unsubscribe_url,ecm_host)
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
    camps = modelcampaign.objects.filter(status = True).order_by("-date_created")
    paginator = Paginator(camps, 5)
    page = request.GET.get('page')
    try:
        camps_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        camps_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        camps_list = paginator.page(paginator.num_pages)
    #pdb.set_trace()
    return render(request, "campain_report.html",{'camps':camps_list,})

def dummy_login_redirect(request):
    return HttpResponse(json.dumps({'status':'login_err'}), content_type="application/json")

@login_required(login_url=get_script_prefix() + "ecm/dummy/login_redirect")
@csrf_protect
def json_report(request):
    '''TEST DATA -- SENDGRID Mimicry
    json_obj=dict()
    json_obj['requests']=1
    json_obj['delivered']=2
    json_obj['opens']=3
    json_obj['unique_opens']=4
    json_obj['clicks']=5
    json_obj['unique_clicks']=6
    json_obj['bounces']=7
    json_obj['unsubscribes']=8
    json_obj['repeat_unsubscribes']=9
    json_obj['invalid_email']=10
    json_obj['blocked']=11
    json_obj['spam_drop']=12
    json_obj['spamreports']=13
    json_obj[unicode('status')] = unicode("success")
    return HttpResponse(json.dumps(json_obj), content_type="application/json")'''
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
    except Exception, e:
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
    paginator = Paginator(camps, 10)
    page = request.GET.get('page')
    try:
        camps_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        camps_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        camps_list = paginator.page(paginator.num_pages)
    return render(request, "view_campaign.html",{'camps':camps_list})

def contacts(request):
    return render(request, "contacts.html")

def contacts_view(request):
    contacts_list = Mail_address.objects.all()
    paginator = Paginator(contacts_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    #return render_to_response(request,'contacts_view.html', {"contacts": maddr})
    return render(request, "contacts_view.html",{'contacts':contacts})


def contacts_statistics(request):
    mlist_obj = Mailing_list.objects.annotate(addrcount=Count('mail_address'))
    paginator = Paginator(mlist_obj, 10)
    page = request.GET.get('page')
    try:
        mlist = paginator.page(page)
    except PageNotAnInteger:
        mlist = paginator.page(1)
    except EmptyPage:
        mlist = paginator.page(paginator.num_pages)
    return render(request, "contact_statistics.html" ,{'mailing_list' : mlist })

def templates(request):
    return render(request, "templates.html")

def home(request):
    return render(request, "home.html")

def templates_new(request):
    def adapt_template(path,obj,request):
        fp = open(path+'index.html','r')
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
    form=mailtemplateform()
    if request.method == "POST":
        form=mailtemplateform(request.POST,request.FILES)
        if form.is_valid():
            #cid = request.POST['cat_id']
            #send_id = request.POST['email_id']
            #send_id='noreply@orange-mailer.net'
            #subj = request.POST['subj']
            obj = form.save()
            try:
                process_zip(obj,request)
                messages.success(request,"Email template saved successfully")
            except Exception, e:
                messages.error(request,"Saving temppate failed ..! ")
                logger.error(" Details :  {0} ".format(e))       
    return render(request, "templates_new.html",{'form':form})

def templates_view(request):
    qset = mailtemplate.objects.all()
    paginator = Paginator(qset, 10)
    page = request.GET.get('page')
    try:
        qset_modified = paginator.page(page)
    except PageNotAnInteger:
        qset_modified = paginator.page(1)
    except EmptyPage:
        qset_modified = paginator.page(paginator.num_pages)
    return render(request, "templates_view.html",{'mailtemplate':qset_modified})

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

def dummy(request):
    return HttpResponse("<h2>Coming soon .. !</h2>", content_type="text/html")


@login_required(login_url=get_script_prefix() + "ecm/dummy/login_redirect")
@csrf_protect
def contacts_search(request):
    squery=request.POST['query']
    results = Mail_address.objects.filter(Q(name__icontains=squery) | Q(mail_id__icontains=squery)).order_by('mail_list')
    if not results:
        return HttpResponse("<p > &nbsp;&nbsp; Your search \""+ squery +"\" returned 0 records, try again ..!</p>", content_type="text/html")
    #pdb.set_trace()
    return render(request, "snippets/contacts_search.html",{'contacts':results})

@login_required(login_url='/login')
@csrf_protect
def contacts_cleanup(request):
    def clean_blocks():
        blocks = BlocksModel.objects.filter(indb=True)
        for block in blocks:
             Mail_address.objects.filter(mail_id__exact=block.email).delete()
             block.indb = False
             block.save()
    def clean_bounces():
        bounces = BouncesModel.objects.filter(indb=True)
        for bounce in bounces:
             Mail_address.objects.filter(mail_id__exact=bounce.email).delete()
             bounce.indb = False
             bounce.save()
    def clean_unsubscribes():
        unsubscribes = UnsubscribesModel.objects.filter(indb=True)
        for unsubscribe in unsubscribes:
             Mail_address.objects.filter(mail_id__exact=unsubscribe.email).delete()
             unsubscribe.indb = False
             unsubscribe.save()
    def clean_spamreports():
        spamreports = SpamreportsModel.objects.filter(indb=True)
        for spamreport in spamreports:
             Mail_address.objects.filter(mail_id__exact=spamreport.email).delete()
             spamreport.indb = False
             spamreport.save()
    form = cleanupform()
    if request.method == "POST":
        if int(request.POST['confirm']) == 0:
            return render(request, "contacts_cleanup.html",{'form':form ,})
        form=cleanupform(request.POST)
        if form.is_valid():
            #pdb.set_trace()
            criteria_list = form.cleaned_data['remove']
            if "blocks" in criteria_list:
                clean_blocks()
            if "bounces" in criteria_list:
                clean_bounces()
            if "unsubscribes" in criteria_list:
                clean_unsubscribes()
            if "spamreports" in criteria_list:
                clean_spamreports()
            messages.success(request,"Cleanup completed successfully ...")
            form = cleanupform()

    return render(request, "contacts_cleanup.html",{'form':form})


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

@csrf_protect
def logout(request):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    pagename='logout'
    auth_logout(request)
    return render(request, 'registration/logout.html',{'pagename':pagename})

