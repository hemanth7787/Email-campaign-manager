from django.contrib import admin
from models import Mailing_list

class Mailing_listAdmin(admin.ModelAdmin):
    pass

admin.site.register(Mailing_list, Mailing_listAdmin)
