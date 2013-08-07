from django import forms
from django.contrib.auth.models import User
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from models import Mail_address, Mailing_list, campaign


class Importform(forms.Form):
	csv_file = forms.FileField(label="Select CSV file")
	cat_drop = forms.ChoiceField(choices=[(x.id, x) for x in Mailing_list.objects.all()])

class campainform(forms.Form):
	t_file = forms.FileField(label="Click to Browse E-mail template")
	subj = forms.CharField(label="Subject")
	#name = forms.CharField(label="Sender name", max_length=30,required=False)
	#email_id= forms.EmailField(label="Sender email id",required=True)

class addcform(forms.Form):
	cat_name = forms.CharField(label="New category name", max_length=30,required=True)
