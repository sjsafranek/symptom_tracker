from django.db import models
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import IntegerField
from django.db.models import ManyToManyField
from django.db.models import OneToOneField
from django.db.models import ForeignKey
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from .therapist import Therapist


class Client(models.Model):
    # Extending User Model Using a One-To-One Link
    ##user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    user = OneToOneField(User, on_delete=models.CASCADE)
    therapist = ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
    
    ## Demographic info
    gender = CharField(
        max_length=8,
        choices=[
            ("Unknown", "Unknown"),
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ],
        default='Unknown'
    )
    sex = CharField(
        max_length=8,
        choices=[
            ("Unknown", "Unknown"),
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ],
        default='Unknown'
    )    
    birth_year = IntegerField(
        default=1900,
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    race = CharField(max_length=50, blank=True, null=True)
    ethnicity = CharField(max_length=50, blank=True, null=True)

    # System info
    # is_active = models.BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def sessions(self):
        return self.session_set.all()

    @property
    def session(self):
        return self.session_set.last()

    @property
    def symptoms(self):
        return self.clientsymptom_set.all()

    # @property
    # def is_active(self):
    #     return self.user.is_active