from itertools import chain

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

    def getTherapists(self):
        return self.therapist_set.all()

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

    def addAgency(self, agency):
        self.agencies.add(agency)
        self.save()

    def getAgencies(self):
        return self.agencies.all()

    def hasAgency(self, agency):
        return agency in self.getAgencies()

    def getClients(self):
        return self.client_set.all()

    def hasClient(self, client):
        return client in self.getClients()

    # normalize data...
    # dedupe symptoms for a session
    # if a session lacks a symptom from a previous session carry the value forward
    def createSession(self, agency, client):
        if self.hasAgency(agency) and self.hasClient(client):
            current = client.getCurrentSession()
            session = Session(client=client, agency=agency, therapist=self)
            session.save()
            if current:
                for symptom in current.getSymptoms():
                    symptom = Symptom(session=session, name=symptom.name, rank=symptom.rank)
                    symptom.save()
            return session
        return None

    def getAllSessions(self):
        return self.session_set.all()

    # normalize data...
    # dedupe symptoms for a session
    # if a session lacks a symptom from a previous session carry the value forward
    def addSymptom(self, client, symptomName):
        if self.hasClient(client) and symptomName not in client.getSymptoms():
            for session in client.getAllSessions():
                symptom = Symptom(session=session, name=symptomName, rank=None)
                symptom.save()
        return None



class Client(models.Model):
    # Extending User Model Using a One-To-One Link
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
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

    def getAllSessions(self):
        return self.session_set.all()

    def getCurrentSession(self):
        return self.session_set.last()

    def getSymptoms(self):
        return list(set(
            chain.from_iterable([
                [
                    symptom.name for symptom in session.getSymptoms()
                ] for session in self.getAllSessions()
            ])
        ))

    def recordSymptom(self, name, rank):
        session = self.getCurrentSession()
        if session:
            for symptom in session.getSymptoms():
                if name == symptom.name:
                    symptom.rank = rank
                    symptom.save()
                    return symptom
        return None

    def getHistory(self):
        history = [
        	{
    			'session_id': session.session_id,
    			'timestamp': session.created_at.timestamp(),
                'symptoms': {
            		symptom.name: symptom.rank
            		for symptom in session.getSymptoms()
            	}
            } for session in self.getAllSessions()
        ]
        return history



class Session(models.Model):
    agency = models.ForeignKey(Agency, null=True, on_delete=models.SET_NULL)
    therapist = models.ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    session_id = AutoField(primary_key=True)
    note = TextField(null=True)
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def getSymptoms(self):
        return self.symptom_set.all()

    def delete(self):
        self.is_deleted = True
        self.save()



class Symptom(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    rank = IntegerField(
        null=True,
        # default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
