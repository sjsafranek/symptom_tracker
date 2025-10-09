from django.db import models
from django.db.models import DateTimeField
from django.db.models import IntegerField
from django.db.models import ForeignKey
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from .client_session import ClientSession
from .client_symptom import ClientSymptom


class ClientSessionSymptomScore(models.Model):
    id = models.AutoField(primary_key=True)
    session = ForeignKey(ClientSession, null=False, on_delete=models.CASCADE)
    symptom = ForeignKey(ClientSymptom, null=False, on_delete=models.CASCADE)
    score = IntegerField(
        null=True,
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('session', 'symptom')
        verbose_name_plural = "Client Session Symptom Scores"

    #def __str__(self):
    #    return '{0} {1} {2}'.format(self.session.date, self.session.client, self.symptom)


