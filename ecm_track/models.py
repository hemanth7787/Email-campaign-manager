from django.db import models
from django.utils.timezone import now

class opens(models.Model):
    campaign_uuid = models.CharField(editable=False, max_length=100)
    template_uuid = models.CharField(editable=False, max_length=100)
    mail_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30, blank=True)
    date_of_creation = models.DateTimeField(editable=False, default=now())
    def __unicode__(self):
        return self.title
