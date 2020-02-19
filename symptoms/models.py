from django.db import models
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import BooleanField
from django.db.models import AutoField
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import TextField
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class Agency(models.Model):
    agency_id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self):
        self.is_deleted = True
        self.save()


class Therapist(models.Model):
    # Extending User Model Using a One-To-One Link
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agencies = models.ManyToManyField(Agency, blank=True)
    therapist_id = AutoField(primary_key=True)
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def delete(self):
        self.is_deleted = True
        self.save()

    def getClients(self):
        return self.client_set.all()

    def getAgencies(self):
        return self.agencies.all()

    def createSession(self, client):
        session = Session(client=client, therapist=self)
        session.save()
        return session


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    therapists = models.ManyToManyField(Therapist, blank=True)
    client_id = AutoField(primary_key=True)
    gender = models.CharField(
        max_length=8,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ]
    )
    age = IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(150)]
    )
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def delete(self):
        self.is_deleted = True
        self.save()

    def getTherapists(self):
        return self.therapists.all()

    def getSessions(self):
        return self.session_set.all()


class Session(models.Model):
    therapist = models.ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    session_id = AutoField(primary_key=True)
    note = TextField(null=True)
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def getSymptoms(self):
        return self.symptom_set.all()

    def createSymptom(self, name, rank):
        symptom = Symptom(session=self, name=name, rank=rank)
        symptom.save()
        return symptom

    def delete(self):
        self.is_deleted = True
        self.save()


class Symptom(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    rank = IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )
