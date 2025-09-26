from django.db import models

from .custom_fields import LowerCaseCharField


class SymptomCategory(models.Model):
    name = LowerCaseCharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name_plural = "Symptom Categories"

    def __str__(self):
        return self.name 
