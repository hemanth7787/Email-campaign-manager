from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import get_script_prefix
from django.http import HttpResponse
from django.conf import settings

import urllib2
import json
from django.utils.encoding import iri_to_uri
#TODO
import logging
logger = logging.getLogger("ecm_console")

from models import BlocksModel, BouncesModel, UnsubscribesModel, SpamreportsModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#import pdb
import logging
logger = logging.getLogger("ecm_console")


@login_required(login_url='/login')
@csrf_protect
def sendgrid_blocks(request):
    qset=BlocksModel.objects.filter(indb=True)
    paginator = Paginator(qset, 5)
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

def sendgrid_bounces(request):
    qset=BouncesModel.objects.filter(indb=True)
    paginator = Paginator(qset, 5)
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

def sendgrid_unsubscribes(request):
    qset=UnsubscribesModel.objects.filter(indb=True)
    paginator = Paginator(qset, 5)
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

def sendgrid_spamreports(request):
    qset=SpamreportsModel.objects.filter(indb=True)
    paginator = Paginator(qset, 5)
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
