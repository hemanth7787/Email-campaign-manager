from django.shortcuts import render, redirect
import base64
import pdb
from models import opens
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ecm_core.forms import campselectform
from ecm_core.models import  campaign as modelcampaign

def open_track(request):
    try:
        key=request.GET['key']

        #encoded = base64.b64encode('data to be encoded')
        #encoded
        #'ZGF0YSB0byBiZSBlbmNvZGVk'
        data = base64.b64decode(key)
        param_list=data.split(",")
        #MAILID NAME CONTACTUUID CAMPAIGNUUID
        opens(mail_id=param_list[0],
            name=param_list[1],
            template_uuid=param_list[2],
            campaign_uuid=param_list[3],
            ).save()
    except:
        pass
    return redirect("/static/assets/ecm.gif")

def open_track_view(request,usid):
    #pdb.set_trace()
    # VERY HARD LOGIC PLEASE REWRITE
    if not usid=='default':
        try:
            hits = opens.objects.filter(campaign_uuid=usid)
            paginator = Paginator(hits, 8)
            page = request.GET.get('page')
            try:
                hits = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                hits = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                hits = paginator.page(paginator.num_pages)
        except:
            pass
    else:
        if request.method == "POST":
            form = campselectform(request.POST) 
            if form.is_valid():
                camp = modelcampaign.objects.get(id=request.POST['campaign'])
                return redirect("/fruits/open-track/"+camp.campaign_uuid+"/")
        else:
            form = campselectform()
            return render(request, "open_camp_select.html",{'form':form})
        
    return render(request, "open_view.html",{'hits':hits})


