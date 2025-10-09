from django.db import models
from django.db.models import DateTimeField
from django.contrib.auth.models import User


class Therapist(models.Model):
    id = models.AutoField(primary_key=True)
    # Extending User Model Using a One-To-One Link
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Therapists"

    def __str__(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name
