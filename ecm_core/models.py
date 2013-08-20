from django.db import models
from django.utils.timezone import now
from uuid import uuid4
import os
from datetime import datetime

class Mail_address(models.Model):
    class Meta:
        verbose_name = 'email address'
        verbose_name_plural = 'email adresses'
    mail_list = models.ForeignKey('Mailing_list')
    mail_id = models.CharField(max_length=30)
    #first_name = models.CharField(max_length=30)
    #middle_name = models.CharField(max_length=30)
    #last_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30, blank=True)
    subscribed = models.BooleanField(default=True)
    uid        = models.CharField(max_length=100)
    def __unicode__(self):
        return self.mail_id
    def save(self, *args, **kwargs):
        if not self.id:
            self.uid = str(uuid4())
        super(Mail_address, self).save(*args, **kwargs)


class Mailing_list(models.Model):
    class Meta:
        verbose_name = 'mailing list'
        verbose_name_plural = 'mailing lists'
    title = models.CharField(max_length=50)
    date_of_creation = models.DateTimeField(editable=False, default=now())
    def __unicode__(self):
        return self.title
	#client

class campaign(models.Model):
    class Meta:
        verbose_name = 'campaign'
        verbose_name_plural = 'campaigns'
    subject      = models.CharField(max_length=100,)#help_text='Email Subject.')
    sender       = models.EmailField(blank=False, null=True)#help_text='Sender\'s Email ID. ( eg:info@gmail.com)')
    mailing_list = models.ManyToManyField(
        'Mailing_list',
        help_text='Select atleast one mailing list :  ',
        blank=True, verbose_name='Target mailing lists',
        #limit_choices_to={'subscribed': True}
        )   
    date_created = models.DateTimeField(editable=False, default=now())
    html = models.TextField(
        verbose_name='Content', #help_text=('Email body'),
        null=True, blank=True
    )
    status       = models.BooleanField(default=False)
    campaign_uuid = models.CharField(editable=False, max_length=100)
    def __unicode__(self):	
        return self.subject
    def category(self):
        return str(self.subject+'-'+self.campaign_uuid)
    def save(self, *args, **kwargs):
        if not self.id:
            self.campaign_uuid = str(uuid4())
        super(campaign, self).save(*args, **kwargs)

class mailtemplate(models.Model):
    def unique_image_name(instance, filename):
        return '/'.join(['thunmbnails',datetime.today().strftime("%B_%Y"), str(uuid4())+os.path.splitext(filename)[1]])
    def unique_file_name(instance, filename):
        return '/'.join(['mailtemplate',datetime.today().strftime("%B_%Y"), str(uuid4())+os.path.splitext(filename)[1]])
    name = models.CharField(max_length=50,null=True)
    zipfile = models.FileField(upload_to=unique_file_name)
    html = models.TextField(verbose_name='Content')
    thumbnail = models.ImageField(upload_to=unique_image_name, blank=True, null=True)
    date_of_creation = models.DateTimeField(editable=False, default=now()) 
    uuid = models.CharField(editable=False, max_length=100)  
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.id:
            self.uuid = str(uuid4())
        super(mailtemplate, self).save(*args, **kwargs)