from django.contrib import admin
from models import Mail_address, Mailing_list, campaign, mailtemplate

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('subject','sender_name','sender','html','campaign_opt')
    #search_fields=['creator__first_name','creator__last_name','creator__username']
    #search_fields=['title']





admin.site.register(campaign, CampaignAdmin)