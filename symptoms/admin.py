from django.contrib import admin

from . import models

admin.site.register(models.Agency)
admin.site.register(models.Therapist)
admin.site.register(models.Client)
admin.site.register(models.ClientSymptom)
admin.site.register(models.Session)
admin.site.register(models.SymptomScore)
