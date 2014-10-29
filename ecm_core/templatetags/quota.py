from django import template
from ecm_core.models import SendgridEmailQuota
register = template.Library()

@register.simple_tag
def remaining():
    quota = SendgridEmailQuota.objects.get(pk=1)
    #return int(quota.remaining())
    if quota.remaining() > (quota.quota/2):
    	return '<a class="alert-success">Remaining : {0} </a>'.format(quota.remaining())
    elif quota.remaining() > (quota.quota/4):
    	return '<a class="alert">Remaining : {0} </a>'.format(quota.remaining())
    else:
    	return '<a class="alert-error">Remaining : {0} </a>'.format(quota.remaining())

@register.simple_tag
def quota():
    quota = SendgridEmailQuota.objects.get(pk=1)
    return int(quota.quota)

@register.simple_tag
def used():
    quota = SendgridEmailQuota.objects.get(pk=1)
    return int(quota.used)