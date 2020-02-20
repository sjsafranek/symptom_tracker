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
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Agencies"

    def getTherapists(self):
        return self.therapist_set.all()

    def __str__(self):
        return '{0}_{1}'.format(self.agency_id, self.name)



class Therapist(models.Model):
    # Extending User Model Using a One-To-One Link
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agencies = models.ManyToManyField(Agency, blank=True)
    therapist_id = AutoField(primary_key=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Therapists"

    def __str__(self):
        return '{0}_{1}'.format(self.therapist_id, self.user.username)

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

    def createSession(self, agency, client):
        # check permissions
        if not self.hasAgency(agency):
            raise ValueError("Insufficient permissions to access agency: {0}", agency.name)

        elif not self.hasClient(client):
            raise ValueError("Insufficient permissions to access client: {0}", client.user.username)

        # get current client session
        current = client.getSession()

        # Prevent new session from being created unless all symptom values are populated
        if not current.isCompleted():
            raise ValueError("Unable to create session. Current session is not completed")

        # create new session and symptom records
        session = Session(client=client, agency=agency, therapist=self)
        session.save()

        # normalize data
        for symptom in client.getSymptoms():
            score = SymptomScore(session=session, symptom=symptom, rank=None)
            score.save()

        # return new session
        return session

    def addSymptom(self, client, name):
        # check permissions
        if not self.hasClient(client):
            raise ValueError("Insufficient permissions to access client: {0}", client.user.username)

        # check if symptom exists
        if client.hasSymptom(name):
            raise ValueError("Symptom already exists: {0}", name)

        # create new symptom
        symptom = ClientSymptom(client=client, name=name)
        symptom.save()

        # normalize symptom data accross past sessions
        for session in client.getSessions():
            score = SymptomScore(session=session, symptom=symptom, rank=None)
            score.save()



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
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Clients"

    def __str__(self):
        return '{0}_{1}'.format(self.client_id, self.user.username)

    def getSessions(self):
        return self.session_set.all()

    def getSession(self):
        return self.session_set.last()

    def getSymptoms(self):
        return self.clientsymptom_set.all()

    def getSymptom(self, name):
        for symptom in self.getSymptoms():
            if name == symptom.name:
                return symptom
        return None

    def hasSymptom(self, name):
        return None != self.getSymptom(name)

    def recordSymptom(self, name, rank):
        session = self.getSession()
        if session:
            for symptom_score in session.getSymptoms():
                if name == symptom_score.symptom.name:
                    symptom_score.rank = rank
                    symptom_score.save()
                    return None
        raise ValueError("Symptom not found: {0}", name)

    def getHistory(self):
        return [
        	{
    			'session_id': session.session_id,
    			'timestamp': session.created_at.timestamp(),
                'symptoms': {
            		symptom_score.symptom.name: symptom_score.rank
            		for symptom_score in session.getSymptoms()
            	}
            } for session in self.getSessions()
        ]



class ClientSymptom(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('client', 'name')
        verbose_name_plural = "Client Symptoms"

    def __str__(self):
        return '{0}_{1}'.format(self.client.client_id, self.name)



class Session(models.Model):
    agency = models.ForeignKey(Agency, null=True, on_delete=models.SET_NULL)
    therapist = models.ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    session_id = AutoField(primary_key=True)
    note = TextField(null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sessions"

    def __str__(self):
        return '{0}_{1}_{2}'.format(self.session_id, self.client.client_id, self.therapist.therapist_id)

    def getSymptoms(self):
        return self.symptomscore_set.all()

    def isCompleted(self):
        for score in self.getSymptoms():
            if not score.rank:
                return False
        return True



class SymptomScore(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    symptom = models.ForeignKey(ClientSymptom, on_delete=models.CASCADE)
    rank = IntegerField(
        null=True,
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Symptom Scores"

    def __str__(self):
        return '{0}_{1}'.format(self.session.session_id, self.symptom.name)
