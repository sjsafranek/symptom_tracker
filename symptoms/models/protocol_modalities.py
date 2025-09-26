from django.db import models
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import DecimalField
from django.db.models import IntegerField
# from django.db.models import TextField    # make a note of each site???
from django.db.models import ForeignKey
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator


from .client_session import ClientSession


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
#

class BaseClientSessionProtocolSiteTrainingModality(models.Model):
    session = ForeignKey(ClientSession, null=False, on_delete=models.CASCADE)
    site = CharField(
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
    # TODO add note???
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class ClientSessionProtocolSiteTrainingILF(BaseClientSessionProtocolSiteTrainingModality):
    frequency_millihertz = DecimalField(
            max_digits=11, 
            decimal_places=6, 
            default=0.000001, 
            null=True,
            validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
        )

    class Meta:
        verbose_name = "Session Protocol Site - ILF"
        verbose_name_plural = "Session Protocol Site - ILF"



class ClientSessionProtocolSiteTrainingAlphaTheta(BaseClientSessionProtocolSiteTrainingModality):   
    alpha_frequency_hertz = DecimalField(
            max_digits=11, 
            decimal_places=6, 
            default=0.000001, 
            null=True,
            validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
        )
    theta_frequency_hertz = DecimalField(
            max_digits=11, 
            decimal_places=6, 
            default=0.000001, 
            null=True,
            validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
        )
    class Meta:
        verbose_name = "Session Protocol Site - AlphaTheta"
        verbose_name_plural = "Session Protocol Site - AlphaTheta"



class ClientSessionProtocolSiteTrainingFrequencyBand(BaseClientSessionProtocolSiteTrainingModality):
    frequency_hertz = DecimalField(
            max_digits=11, 
            decimal_places=6, 
            default=0.000001, 
            null=True,
            validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
        )

    class Meta:
        verbose_name = "Session Protocol Site - FrequencyBand"
        verbose_name_plural = "Session Protocol Site - FrequencyBand"



class ClientSessionProtocolSiteTrainingSynchrony(BaseClientSessionProtocolSiteTrainingModality):
    frequency_millihertz = DecimalField(
            max_digits=11, 
            decimal_places=6, 
            default=0.000001, 
            null=True,
            validators=[MinValueValidator(0.000001), MaxValueValidator(40000)]            
        )

    class Meta:
        verbose_name = "Session Protocol Site - Synchrony"
        verbose_name_plural = "Session Protocol Site - Synchrony"

