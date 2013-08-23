from django import forms
from django.contrib.auth.models import User
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from models import Mail_address, Mailing_list, campaign, mailtemplate 
from django.contrib.admin.widgets import FilteredSelectMultiple


class Importform(forms.Form):
	csv_file = forms.FileField(label="Select CSV file")
	name = forms.CharField(label="Mailing list name")
	#mailing_list = forms.ModelChoiceField(queryset=Mailing_list.objects.all())

class campainform(forms.Form):
	t_file = forms.FileField(label="Click to Browse E-mail template")
	subj = forms.CharField(label="Subject")
	#name = forms.CharField(label="Sender name", max_length=30,required=False)
	#email_id= forms.EmailField(label="Sender email id",required=True)

class addcform(forms.Form):
	cat_name = forms.CharField(label="New category name", max_length=30,required=True)


class ListBasketForm(forms.ModelForm): 
    CHOICES = (('T', 'Template',),('P', 'Plain text',)) #,  ('W', 'Wysisyg editor',)
    content_type = forms.ChoiceField(widget=forms.RadioSelect(
    attrs={'onclick': 'content_select(value);'},)
    , choices=CHOICES)
    mailing_list = forms.ModelMultipleChoiceField(queryset=Mailing_list.objects.all())
    template = forms.ModelChoiceField(queryset=mailtemplate.objects.all(),empty_label=None)
    #html = forms.CharField(widget=forms.Textarea(attrs={'rows':'10', 'cols': '30'}))

    class Meta:
        model = campaign
        fields = ('subject','sender','content_type','template','html','mailing_list',)

class mailtemplateform(forms.ModelForm): 
    class Meta:
        model = mailtemplate
        fields = ('name','thumbnail','zipfile')

class campselectform(forms.Form):
    campaign = forms.ModelChoiceField(queryset=campaign.objects.all().order_by("-date_created"),empty_label=None)