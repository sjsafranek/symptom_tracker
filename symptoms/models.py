from itertools import chain

from django.db import models
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import BooleanField
from django.db.models import AutoField
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import TextField
from django.db.models import DecimalField
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
# from guardian.shortcuts import assign_perm



class Agency(models.Model):
    agency_id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    # address
    # phonenumber
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Agencies"

    def getTherapists(self):
        return self.therapist_set.all()

    def __str__(self):
        return 'A{0}-{1}'.format(self.agency_id, self.name)



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
        return 'T{0}U{1}'.format(self.therapist_id, self.user.alias())

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

    def createSession(self, client):
        if not self.hasClient(client):
            raise ValueError("Insufficient permissions to access client: {0}", client)

        return Session.create(therapist=self, client=client)

    def addSymptom(self, client, name):
        # check permissions
        if not self.hasClient(client):
            raise ValueError("Insufficient permissions to access client: {0}", client)

        # check if symptom exists
        if client.hasSymptom(name):
            raise ValueError("Symptom already exists: {0}", name)

        # create new symptom
        symptom = ClientSymptom(client=client, name=name)
        symptom.save()

        # normalize symptom data accross past sessions
        # for session in client.getSessions():
        for session in client.sessions:
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
    # birthday
    # phonenumber
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Clients"

    def __str__(self):
        return 'C{0}U{1}'.format(self.client_id, self.user.alias())

    @property
    def sessions(self):
        return self.session_set.all()

    @property
    def session(self):
        return self.session_set.last()

    @property
    def symptoms(self):
        return self.clientsymptom_set.all()

    def getSymptom(self, name):
        for symptom in self.symptoms:
            if name == symptom.name:
                return symptom
        return None

    def hasSymptom(self, name):
        return None != self.getSymptom(name)

    def recordSymptom(self, name, rank):
        if self.session:
            for symptom_score in self.session.symptoms:
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
                    for symptom_score in session.symptoms
            	}
            } for session in self.sessions
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
        return 'CS{0}-{1}'.format(self.client.client_id, self.name)



class Session(models.Model):
    therapist = models.ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    session_id = AutoField(primary_key=True)
    note = TextField(null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sessions"

    def __str__(self):
        return 'S{0}-{1}'.format(self.session_id, self.client)

    @classmethod
    def create(cls, therapist, client):
        oldSession = client.session

        # Prevent new session from being created unless all symptom values are populated
        if oldSession and not oldSession.complete:
            raise ValueError("Unable to create session. Current session is not completed")

        # create new session and symptom records
        newSession = cls(client=client, therapist=therapist)
        newSession.save()

        # normalize data
        for symptom in client.symptoms:
            score = SymptomScore(session=newSession, symptom=symptom, rank=None)
            score.save()

        # return new session
        return newSession

    @property
    def symptoms(self):
        return self.symptomscore_set.all()

    @property
    def complete(self):
        for score in self.symptoms:
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
        return 'SS{0}-{1}'.format(self.session.session_id, self.symptom)



class NeurofeedbackProtocols(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    ILF_site = models.CharField(
        null=True,
        default=None,
        max_length=8,
        choices=[
            ("T3-T4", "T3-T4"),
            ("T4-P4", "T4-P4"),
            ("T4-FP2", "T4-FP2"),
            ("T3-FP1", "T3-T4"),
            ("T3-03", "T3-T4"),
            ("T4-02", "T3-T4"),
            ("T4-F6", "T3-T4"),
            ("T4-F8", "T3-T4"),
            ("T3-F7", "T3-T4"),
            ("T3-F3", "T3-T4"),
            ("T3-T5", "T3-T4"),
            ("T3-01", "T3-T4"),
            ("FP1-FP2", "T3-T4"),
            ("P3-P4", "T3-T4"),
            ("01-01", "T3-T4"),
            ("FP1-P3/FP2-P4", "FP1-P3/FP2-P4"),
            ("F3-P3/F4-P4", "F3-P3/F4-P4"),
            ("T3-P3/T4-P4", "T3-P3/T4-P4")
        ]
    )

    ILF_frequency = models.DecimalField(
                            null=True,
                            max_digits=2,
                            decimal_places=5,
                            default=None,
                            validators=[MinValueValidator(0.0001), MaxValueValidator(40.0000)])

    # SYN_site
    # SYN_frequency

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
