import json
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.urls import reverse

from .models import Therapist
from .models import Client
from .models import ClientSession
from .models import ClientSymptom
from .models import ClientSessionProtocolSiteTrainingILF
from .models import ClientSessionProtocolSiteTrainingAlphaTheta
from .models import ClientSessionProtocolSiteTrainingFrequencyBand
from .models import ClientSessionProtocolSiteTrainingSynchrony


@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(
        request, 
        'dashboard.html', 
        { 
            'therapists': Therapist.objects.all().order_by('user__last_name', 'user__first_name')
        }
    )

@login_required(login_url='/accounts/login/')
def client_dashboard(request, client_id):
    client = Client.objects.get(id=client_id)
    return render(
        request, 
        'dashboard.html', 
        { 
            'client': {
                'id': client.id
            }
        }
    )


@login_required
def get_clients_by_therapist(request, therapist_id):
    therapist = Therapist.objects.filter(id=therapist_id).get()
    clients = therapist.client_set.filter(user__is_active=True).all()
    return JsonResponse({
        'status': 'ok',
        'data': {
            'clients': [
                {
                    'id': client.id,
                    'name': client.user.get_full_name()
                } for client in clients
            ]
        }
    })


@login_required
def get_sessions_by_client(request, client_id):
    sessions = ClientSession.objects.filter(client__id=client_id).order_by('date').all()
    return JsonResponse({
        'status': 'ok',
        'data': {
            'sessions': [
                {
                    'id': session.id,
                    'date': session.date,
                    'number': session.number,
                    'no_show': session.no_show,
                    'symptom_scores': [
                        {
                            'name': score.symptom.description,
                            'score': score.score
                        } for score in session.clientsessionsymptomscore_set.all()
                    ]
                } for session in sessions
            ]
        }
    })


@login_required
def get_symptoms_by_client(request, client_id):
    symptoms = ClientSymptom.objects.filter(client__id=client_id).all()
    return JsonResponse({
        'status': 'ok',
        'data': {
            'symptoms': [
                {
                    'id': symptom.id,
                    'name': symptom.description,
                    'is_active': symptom.is_active,
                    'baseline': {
                        'goodweek': symptom.baseline_goodweek,
                        'badweek': symptom.baseline_badweek,
                        'usualweek': symptom.baseline_usualweek
                    },
                    'categories': [
                        category.name for category in symptom.symptom_categories.all()
                    ]
                } for symptom in symptoms
            ]
        }
    })


@login_required
def get_protocol_by_session(request, session_id):

    protocol = []
    protocol += ClientSessionProtocolSiteTrainingILF.objects.filter(session__id=session_id).all()
    protocol += ClientSessionProtocolSiteTrainingAlphaTheta.objects.filter(session__id=session_id).all()
    protocol += ClientSessionProtocolSiteTrainingFrequencyBand.objects.filter(session__id=session_id).all()
    protocol += ClientSessionProtocolSiteTrainingSynchrony.objects.filter(session__id=session_id).all()
    protocol = sorted(protocol, key=lambda protocol: protocol.order)

    return JsonResponse({
        'status': 'ok',
        'data': {
            'protocol': [
                {
                    'type': modality.type,
                    'site': modality.site,
                    'duration': modality.duration_minutes,
                    'order': modality.order,
                    'notes': modality.notes,
                    'settings': modality.settings
                } for modality in protocol
            ]
        }
    })


