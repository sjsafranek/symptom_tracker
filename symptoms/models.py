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
from django.db.models import DateField
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User




class LowerCaseCharField(CharField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value is not None:
            return value.lower()
        return value





class Therapist(models.Model):
    # Extending User Model Using a One-To-One Link
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Therapists"

    def __str__(self):
        #return 'T{0}U{1}'.format(self.therapist_id, self.user.alias())
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name



class SymptomCategory(models.Model):
    name = LowerCaseCharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name_plural = "Symptom Categories"

    def __str__(self):
        return self.name 



class Client(models.Model):
    # Extending User Model Using a One-To-One Link
    ##user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
    
    ## Demographic info
    gender = models.CharField(
        max_length=8,
        choices=[
            ("Unknown", "Unknown"),
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ],
        default='Unknown'
    )
    sex = models.CharField(
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
    race = models.CharField(max_length=50, blank=True, null=True)
    ethnicity = models.CharField(max_length=50, blank=True, null=True)

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



class ClientSymptom(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    symptom_categories = models.ManyToManyField(SymptomCategory, blank=False)
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
    is_active = models.BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('client', 'description')
        verbose_name_plural = "Client Symptoms"

    def __str__(self):
        return '{0} {1}'.format(self.client, self.description)



class ClientNote(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
    note = models.TextField(blank=False, null=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Client Notes"

    def __str__(self):
        chunk = self.note[0:16]
        if len(chunk) < len(self.note):
            chunk += '...'
        return chunk

    @property
    def display(self):
        return str(self)



class ClientSession(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)    
    therapist = models.ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
    date = models.DateField()
    no_show = models.BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Client Sessions"

    def __str__(self):
        return '{0} {1}'.format(self.date, self.client)

    @property
    def number(self):
        if self.no_show:
            return None
        c=0
        for session in self.client.clientsession_set.filter(no_show=False).order_by('date'):
            print(session)
            if self.id == session.id:
                return c
            c += 1
        return None



class ClientSessionSymptomScore(models.Model):
    session = models.ForeignKey(ClientSession, null=False, on_delete=models.CASCADE)
    symptom = models.ForeignKey(ClientSymptom, null=False, on_delete=models.CASCADE)
    score = IntegerField(
        null=True,
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('session', 'symptom')
        verbose_name_plural = "Client Session Symptom Scores"

    #def __str__(self):
    #    return '{0} {1} {2}'.format(self.session.date, self.session.client, self.symptom)



# class ClientSessionProtocolSiteTraining(models.Model):
#     session = models.ForeignKey(ClientSession, null=False, on_delete=models.CASCADE)
#     site = models.CharField(
#             max_length=32,
#             choices=[
#                 ("Unknown", "Unknown")
#             ],
#             default='Unknown'
#         )
#     modality = models.CharField(
#             max_length=16,
#             choices=[
#                 ("ILF", "ILF"),                     # mlhz
#                 ("AlphaTheta", "AlphaTheta"),       # alpha 8-13 hz, theta 4-8 hz
#                 ("FrequencyBand", "FrequencyBand"), # hz 
#                 ("Synchrony", "Synchrony")          # 0.05 - 0.01 mlhz, 10 mlhz, 40 mlhz
#             ],
#             default='ILF'
#         )
#     duration_minutes = IntegerField(
#             null=False,
#             validators=[MinValueValidator(0), MaxValueValidator(120)]
#         )    
#     frequency_millihertz = models.DecimalField(
#             max_digits=11, 
#             decimal_places=6, 
#             default=0.000001, 
#             null=True,
#             validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
#         )
#     created_at = DateTimeField(auto_now_add=True)
#     updated_at = DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = "Client Session Protocol Site Training"



class ClientSessionProtocolSiteTraining(models.Model):
    session = models.ForeignKey(ClientSession, null=False, on_delete=models.CASCADE)
    site = models.CharField(
            max_length=32,
            choices=[
                ("Unknown", "Unknown")
            ],
            default='Unknown'
        )
    duration_minutes = IntegerField(
            null=False,
            validators=[MinValueValidator(0), MaxValueValidator(120)]
        )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class ClientSessionProtocolSiteTrainingILF(ClientSessionProtocolSiteTraining):
    frequency_millihertz = models.DecimalField(
            max_digits=11, 
            decimal_places=6, 
            default=0.000001, 
            null=True,
            validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
        )

    class Meta:
        verbose_name = "Session Protocol Site - ILF"
        verbose_name_plural = "Session Protocol Site - ILF"



class ClientSessionProtocolSiteTrainingAlphaTheta(ClientSessionProtocolSiteTraining):   
    alpha_frequency_hertz = models.DecimalField(
            max_digits=11, 
            decimal_places=6, 
            default=0.000001, 
            null=True,
            validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
        )
    theta_frequency_hertz = models.DecimalField(
            max_digits=11, 
            decimal_places=6, 
            default=0.000001, 
            null=True,
            validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
        )
    class Meta:
        verbose_name = "Session Protocol Site - AlphaTheta"
        verbose_name_plural = "Session Protocol Site - AlphaTheta"



class ClientSessionProtocolSiteTrainingFrequencyBand(ClientSessionProtocolSiteTraining):
    frequency_hertz = models.DecimalField(
            max_digits=11, 
            decimal_places=6, 
            default=0.000001, 
            null=True,
            validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
        )

    class Meta:
        verbose_name = "Session Protocol Site - FrequencyBand"
        verbose_name_plural = "Session Protocol Site - FrequencyBand"



class ClientSessionProtocolSiteTrainingSynchrony(ClientSessionProtocolSiteTraining):
    frequency_millihertz = models.DecimalField(
            max_digits=11, 
            decimal_places=6, 
            default=0.000001, 
            null=True,
            validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
        )

    class Meta:
        verbose_name = "Session Protocol Site - Synchrony"
        verbose_name_plural = "Session Protocol Site - Synchrony"

