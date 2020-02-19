from django.contrib import admin

from . import models

admin.site.register(models.Agency)
admin.site.register(models.Therapist)
admin.site.register(models.Client)
