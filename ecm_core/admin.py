from django.contrib import admin
from models import Mail_address, Mailing_list, campaign, mailtemplate

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('subject','sender_name','sender','html','campaign_opt')
    #search_fields=['creator__first_name','creator__last_name','creator__username']
    #search_fields=['title']


class Mail_addressAdmin(admin.ModelAdmin):
    list_display = ('mail_id','First_Name','Middle_Name','Last_Name','Date_of_Birth',
    	'Gender','Country','mail_list',
    	#'City','Direct_Phone','Mobile','Address_1','Address_2',
    	#'Zip','Telephone_1','Telephone_2','Company',
    	#'Job_Title','Website','mail_list',
    	'subscribed','spam_flag','unsub_flag','block_flag','bounce_flag')
    search_fields=['First_Name','Middle_Name','Last_Name','mail_id']
    list_filter = ['subscribed','spam_flag','unsub_flag','block_flag','bounce_flag','mail_list']


admin.site.register(campaign, CampaignAdmin)
admin.site.register(Mail_address, Mail_addressAdmin)
