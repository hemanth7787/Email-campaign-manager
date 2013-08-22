from django.shortcuts import render, redirect
import base64
import pdb
from models import opens

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

