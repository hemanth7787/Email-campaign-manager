from django.contrib import admin
from models import CampaignSchedule, Mail_address, Mailing_list, campaign, mailtemplate, SendgridEmailQuota

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

class SendgridEmailQuotaAdmin(admin.ModelAdmin):
    list_display = ('quota','used','remaining')
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True
    def has_delete_permission(self, request, obj=None):
        return False if self.model.objects.count() <= 1 else True
    def get_actions(self, request):
        actions = super(SendgridEmailQuotaAdmin, self).get_actions(request)
        if(self.model.objects.count() <= 1):
            del actions['delete_selected']
        return actions

from django.utils.timezone import localtime

class CampaignScheduleAdmin(admin.ModelAdmin):
    list_display = ('campaign','date')
    def date(self,obj):
        return localtime(obj.schedule_date).strftime("%d-%m-%Y %H:%M")


admin.site.register(CampaignSchedule, CampaignScheduleAdmin)
admin.site.register(SendgridEmailQuota, SendgridEmailQuotaAdmin)
admin.site.register(campaign, CampaignAdmin)
admin.site.register(Mail_address, Mail_addressAdmin)

