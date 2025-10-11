from django.contrib.auth.models import User

from .models import ClientSessionProtocolSiteTrainingILF
from .models import ClientSessionProtocolSiteTrainingAlphaTheta
from .models import ClientSessionProtocolSiteTrainingFrequencyBand
from .models import ClientSessionProtocolSiteTrainingSynchrony


def getUserByUsername(username):
    return User.objects.filter(username=username).first()


def fetchProtocolBySessionId(session_id):
    protocol = []
    protocol += ClientSessionProtocolSiteTrainingILF.objects.filter(session__id=session_id).all()
    protocol += ClientSessionProtocolSiteTrainingAlphaTheta.objects.filter(session__id=session_id).all()
    protocol += ClientSessionProtocolSiteTrainingFrequencyBand.objects.filter(session__id=session_id).all()
    protocol += ClientSessionProtocolSiteTrainingSynchrony.objects.filter(session__id=session_id).all()
    protocol = sorted(protocol, key=lambda protocol: protocol.order)
    return protocol
