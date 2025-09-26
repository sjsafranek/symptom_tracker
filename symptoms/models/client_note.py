from django.db import models
from django.db.models import DateTimeField
from django.db.models import TextField
from django.db.models import ForeignKey

from .therapist import Therapist
from .client import Client


class ClientNote(models.Model):
    client = ForeignKey(Client, on_delete=models.CASCADE)
    therapist = ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
    note = TextField(blank=False, null=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Client Notes"

    def __str__(self):
        chunk = self.note[0:16]
        if len(chunk) < len(self.note):
            chunk += '...'
        return chunk

    @property
    def display(self):
        return str(self)
