from django import forms


class cleanupform(forms.Form):
    CHOICES = (('blocks', 'Blocks',),
               ('bounces', 'Bounces',),
               ('unsubscribes', 'Unsubscribes',),
               ('spamreports', 'Spam Reports',))
    OPTIONS = (('L', 'Remove from block/bounce/etc list only',), ('C', 'Also remove from saved contacts',))
    remove = forms.MultipleChoiceField(choices=CHOICES,
                                       widget=forms.CheckboxSelectMultiple,
                                       label="Select criteria")
    options = forms.ChoiceField(widget=forms.RadioSelect, choices=OPTIONS)
