from django.shortcuts import render  #, get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from forms import cleanupform
# from django.core.urlresolvers import get_script_prefix
# from django.http import HttpResponse
# from django.conf import settings

# import urllib2
# import json
# from django.utils.encoding import iri_to_uri
#TODO
import logging
logger = logging.getLogger("ecm_console")

from models import BlocksModel, BouncesModel, UnsubscribesModel, SpamreportsModel
from ecm_core.models import Mail_address
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='/login')
@csrf_protect
def sendgrid_blocks(request):
    qset=BlocksModel.objects.filter()
    paginator = Paginator(qset, 15)
    page = request.GET.get('page')
    try:
        qset_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        qset_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        qset_list = paginator.page(paginator.num_pages)
    return render(request, "sendgridapi/blocks.html",{'qset':qset_list})

@login_required(login_url='/login')
@csrf_protect
def sendgrid_bounces(request):
    qset=BouncesModel.objects.filter()
    paginator = Paginator(qset, 15)
    page = request.GET.get('page')
    try:
        qset_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        qset_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        qset_list = paginator.page(paginator.num_pages)
    return render(request, "sendgridapi/bounces.html",{'qset':qset_list})

@login_required(login_url='/login')
@csrf_protect
def sendgrid_unsubscribes(request):
    qset=UnsubscribesModel.objects.filter()
    paginator = Paginator(qset, 15)
    page = request.GET.get('page')
    try:
        qset_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        qset_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        qset_list = paginator.page(paginator.num_pages)
    return render(request, "sendgridapi/unsubscribes.html",{'qset':qset_list})

@login_required(login_url='/login')
@csrf_protect
def sendgrid_spamreports(request):
    qset=SpamreportsModel.objects.filter()
    paginator = Paginator(qset, 15)
    page = request.GET.get('page')
    try:
        qset_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        qset_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        qset_list = paginator.page(paginator.num_pages)
    return render(request, "sendgridapi/spamreports.html",{'qset':qset_list})

@login_required(login_url='/login')
@csrf_protect
def contacts_cleanup(request):
    def clean_blocks(delete_contacts=False):
        blocks = BlocksModel.objects.all()
        if delete_contacts:
            addr_list = blocks.values_list('email', flat=True)
            Mail_address.objects.filter(mail_id__in=addr_list).delete()
            #for block in blocks:
            #    Mail_address.objects.filter(mail_id__exact=block.email).delete()
        blocks.delete()

    def clean_bounces(delete_contacts=False):
        bounces = BouncesModel.objects.all()
        if delete_contacts:
            addr_list = bounces.values_list('email', flat=True)
            Mail_address.objects.filter(mail_id__in=addr_list).delete()
            # for bounce in bounces:
            #     Mail_address.objects.filter(mail_id__exact=bounce.email).delete()
        bounces.delete()

    def clean_unsubscribes(delete_contacts=False):
        unsubscribes = UnsubscribesModel.objects.all()
        if delete_contacts:
            addr_list = unsubscribes.values_list('email', flat=True)
            Mail_address.objects.filter(mail_id__in=addr_list).delete()
            # for unsubscribe in unsubscribes:
            #     Mail_address.objects.filter(mail_id__exact=unsubscribe.email).delete()
        unsubscribes.delete()

    def clean_spamreports(delete_contacts=False):
        spamreports = SpamreportsModel.objects.all()
        if delete_contacts:
            addr_list = spamreports.values_list('email', flat=True)
            Mail_address.objects.filter(mail_id__in=addr_list).delete()
            # for spamreport in spamreports:
            #     Mail_address.objects.filter(mail_id__exact=spamreport.email).delete()
        spamreports.delete()

    form = cleanupform({'options': 'L', 'remove': ['blocks', 'bounces', 'unsubscribes', 'spamreports']})
    if request.method == "POST":
        if int(request.POST['confirm']) == 0:
            return render(request, "contacts_cleanup.html",{'form':form ,})
        form = cleanupform(request.POST)
        if form.is_valid():
            criteria_list = form.cleaned_data['remove']
            if "C" in form.cleaned_data['options']:
                remove_contacts = True
            else:
                remove_contacts = False
            if "blocks" in criteria_list:
                clean_blocks(remove_contacts)
            if "bounces" in criteria_list:
                clean_bounces(remove_contacts)
            if "unsubscribes" in criteria_list:
                clean_unsubscribes(remove_contacts)
            if "spamreports" in criteria_list:
                clean_spamreports(remove_contacts)
            messages.success(request,"Cleanup completed successfully ...")
            form = cleanupform()

    return render(request, "sendgridapi/contacts_cleanup.html",{'form':form})