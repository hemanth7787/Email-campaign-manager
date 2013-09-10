from django.db import models
from django.utils.timezone import now
from uuid import uuid4
import os
from datetime import datetime

class Mail_address(models.Model):
    class Meta:
        verbose_name = 'email address'
        verbose_name_plural = 'email adresses'
    CHOICES = (('M', 'Male',),('F', 'Female',))
    First_Name = models.CharField(max_length=30, blank=True,null=True )
    Middle_Name = models.CharField(max_length=30, blank=True, null=True)
    Last_Name = models.CharField(max_length=30, blank=True, null=True)
    Date_of_Birth = models.DateField(blank=True,null=True)
    Gender = models.CharField(max_length=5, choices=CHOICES, blank=True,null=True)
    mail_id = models.EmailField(verbose_name='email')
    Country = models.CharField(max_length=30, blank=True,null=True)
    City = models.CharField(max_length=30, blank=True,null=True)
    Direct_Phone = models.CharField(max_length=20, blank=True,null=True)
    Mobile = models.CharField(max_length=15, blank=True,null=True)
    Address_1 = models.TextField(blank = True,null=True)
    Address_2 = models.TextField(blank = True,null=True)
    Zip = models.CharField(max_length=15, blank=True,null=True)
    Telephone_1 = models.CharField(max_length=15, blank=True,null=True)
    Telephone_2 = models.CharField(max_length=15, blank=True,null=True)
    Company = models.CharField(max_length=30, blank=True,null=True)
    Job_Title = models.CharField(max_length=30, blank=True,null=True)
    Website = models.CharField(max_length=30, blank=True,null=True)
    mail_list = models.ForeignKey('Mailing_list',verbose_name='group')
    #name = models.CharField(max_length=30, blank=True)
    subscribed = models.BooleanField(default=True)
    uid        = models.CharField(max_length=100)
    def __unicode__(self):
        return self.mail_id
    def full_name(self):
        return self.First_Name+" "+self.Middle_Name+" "+self.Last_Name
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
    thumbnail = models.ImageField(upload_to=unique_image_name, blank=True, null=True, verbose_name='Optional Thumbnail')
    date_of_creation = models.DateTimeField(editable=False, default=now()) 
    uuid = models.CharField(editable=False, max_length=100)  
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.id:
            self.uuid = str(uuid4())
        super(mailtemplate, self).save(*args, **kwargs)