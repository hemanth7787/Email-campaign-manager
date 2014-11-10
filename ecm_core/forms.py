from django import forms
from django.contrib.auth.models import User
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from models import Mail_address, Mailing_list, campaign, mailtemplate 
from django.contrib.admin.widgets import FilteredSelectMultiple

from ckeditor.widgets import CKEditorWidget

#NEEDED
class Importform(forms.Form):
    CHOICES = (('E', 'Append to existing group',),('N', 'Create new group',))
    csv_file = forms.FileField(label="Select CSV file")
    options = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'onclick': 'content_select(value);'},),
        choices=CHOICES)
    name = forms.CharField(label="Group name",required=False)
    group = forms.ModelChoiceField(queryset=Mailing_list.objects.all().order_by("-date_of_creation"),required=False)

class addcform(forms.Form):
	cat_name = forms.CharField(label="New category name", max_length=30,required=True)

#NEEDED
class ListBasketForm(forms.ModelForm): 
    CHOICES = (('P', 'Rich text',),('T', 'Template',))
    SEND_OPT = (('Q', 'Quick send',),('N', 'Normal send',))
    CAMP_OPT = (('R', 'Run',),('S', 'Save',),('T', 'Test',))
    RUN_OPT = (('I', 'Immediate',),('S', 'Schedule [beta] ',))
    content_type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onclick': 'content_select(value);'},)
    , choices=CHOICES)
    mailing_list = forms.ModelMultipleChoiceField(queryset=Mailing_list.objects.all(),label='Target Groups')
    template = forms.ModelChoiceField(queryset=mailtemplate.objects.all(),empty_label=None)
    send_options = forms.ChoiceField(widget=forms.RadioSelect()
    , choices=SEND_OPT)
    run_mode = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'onclick': 'mode_select(value);'},), choices=RUN_OPT,)
    schedule_date = forms.CharField(required=False)
    html = forms.CharField(widget=CKEditorWidget(),label='Content',required=False)
    campaign_opt = forms.ChoiceField(choices=CAMP_OPT,widget = forms.HiddenInput())

    class Meta:
        model = campaign
        fields = ('campaign_name','subject','sender_name','sender','content_type','template',
            'html','mailing_list','campaign_opt','send_options')

class mailtemplateform(forms.ModelForm): 
    class Meta:
        model = mailtemplate
        fields = ['name','zipfile']

class campselectform(forms.Form): # For opentrack
    campaign = forms.ModelChoiceField(queryset=campaign.objects.filter(status=True).order_by("-date_created"),empty_label=None)

class cleanupform(forms.Form):
    CHOICES = (('blocks', 'Blocks',),('bounces', 'Bounces',),('unsubscribes', 'Unsubscribes',),('spamreports', 'Spam Reports',))
    remove = forms.MultipleChoiceField(choices=CHOICES,widget=forms.CheckboxSelectMultiple,label="Select criteria")

class singlecontactform(forms.ModelForm):
    class Meta:
        model = Mail_address
        fields = ['First_Name','Middle_Name','Last_Name','Date_of_Birth',
        'Gender','mail_id','options','name','mail_list','Country','City','Direct_Phone','Mobile','Address_1',
        'Address_2','Zip','Telephone_1','Telephone_2','Company','Job_Title','Website']
    CHOICES = (('E', 'Append to existing group',),('N', 'Create new group',))
    options = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'onclick': 'mlist_options(value);'},),
        choices=CHOICES)
    mail_list = forms.ModelChoiceField(queryset=Mailing_list.objects.all().order_by("-date_of_creation"),required=False,label="Group")
    name = forms.CharField(label="Group name",required=False)
    Date_of_Birth = forms.DateField(widget=forms.DateInput(format = '%d-%m-%Y'), input_formats=('%d-%m-%Y',),
     label = 'Date of Birth (dd-mm-yyyy)',required=False)


class listselectform(forms.Form):
    Mailing_list = forms.ModelChoiceField(queryset=Mailing_list.objects.all().order_by("-date_of_creation"),empty_label=None)

class AddContactForm(forms.Form):

    name = forms.CharField(max_length=30)
    mail_id = forms.CharField(max_length=30)
    CHOICES = (('E', 'Add to existing group',),('N', 'Create new group',)) #,  ('W', 'Wysisyg editor',)
    Options = forms.ChoiceField(widget=forms.RadioSelect(
    attrs={'onclick': 'content_select(value);'},)
    , choices=CHOICES)
    Mailing_list = forms.ModelChoiceField(label="Group",queryset=Mailing_list.objects.all().order_by("-date_of_creation"),empty_label=None)
    Group_name = forms.CharField(label="Group name",max_length=30, required=False)

class campeditform(forms.ModelForm):
    class Meta:
        model = campaign
        fields = ('campaign_name','subject','sender_name','sender','mailing_list')