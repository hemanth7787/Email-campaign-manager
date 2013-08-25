from django.db import models

class BlocksModel(models.Model):
    class Meta:
        verbose_name = 'Blocks'
    email = models.CharField(max_length=30, unique=True)
    indb = models.BooleanField(default=True)
    def __unicode__(self):
        return self.email

class BouncesModel(models.Model):
    class Meta:
        verbose_name = 'Bounces'
    email = models.CharField(max_length=30)
    indb = models.BooleanField(default=True)
    def __unicode__(self):
        return self.email

class UnsubscribesModel(models.Model):
    class Meta:
        verbose_name = 'Unsubscribes'
    email = models.CharField(max_length=30)
    indb = models.BooleanField(default=True)
    def __unicode__(self):
        return self.email

class SpamreportsModel(models.Model):
    class Meta:
        verbose_name = 'Spam Reports'
    email = models.CharField(max_length=30)
    indb = models.BooleanField(default=True)
    def __unicode__(self):
        return self.email

class JobstatusModel(models.Model):
    class Meta:
        verbose_name = 'DB Update Job Status'
    lastrun = models.DateTimeField(editable=False, null=True) # Now() = UTC , datetime.today() = settings TZ = America/Chicago
    purpose = models.CharField(max_length=30)
