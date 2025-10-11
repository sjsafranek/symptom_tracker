from django.db import models
from django.db.models import BooleanField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import DecimalField
from django.db.models import ForeignKey

from .client import Client
from .therapist import Therapist


class ClientSession(models.Model):
    id = models.AutoField(primary_key=True)
    client = ForeignKey(Client, null=True, on_delete=models.CASCADE)    
    therapist = ForeignKey(Therapist, null=True, on_delete=models.SET_NULL, blank=True)
    date = models.DateField()
    no_show = models.BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        # unique_together = ('client', 'date')
        verbose_name_plural = "Client Sessions"

    def __str__(self):
        return '{0} {1}'.format(self.date, self.client)

    @property
    def number(self):
        if self.no_show:
            return None
        c=0
        for session in self.client.clientsession_set.filter(no_show=False).order_by('date'):
            if self.id == session.id:
                return c
            c += 1
        return None
