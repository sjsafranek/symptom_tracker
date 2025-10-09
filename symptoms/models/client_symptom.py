from django.db import models
from django.db.models import BooleanField
from django.db.models import DateTimeField
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import ManyToManyField
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from .client import Client
from .symptom_category import SymptomCategory


class ClientSymptom(models.Model):
    id = models.AutoField(primary_key=True)
    client = ForeignKey(Client, on_delete=models.CASCADE)
    description = CharField(max_length=50)
    symptom_categories = ManyToManyField(SymptomCategory, blank=False)
    baseline_goodweek = IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    baseline_badweek = IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    baseline_usualweek = IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('client', 'description')
        verbose_name_plural = "Client Symptoms"

    def __str__(self):
        return '{0} {1}'.format(self.client, self.description)
