import base64
import pdb
def TrackCode(host,mobj,cuuid):
    params=str(mobj.mail_id+','+mobj.name+','+mobj.uid+','+cuuid)
    encoded=base64.b64encode(params)
    code = '<img src="{0}" alt="" width="1" height="1" border="0" style="height:1px !important;width:1px\
    !important;border-width:0 !important;margin-top:0 !important;margin-bottom:0 !important;margin-right:0 \
    !important;margin-left:0 !important;padding-top:0 !important;padding-bottom:0 !important;padding-right:0 \
    !important;padding-left:0 !important;"/>'.format(host+'/fruits/open?key='+encoded)
    return code
