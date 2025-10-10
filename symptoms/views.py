import json
from datetime import datetime

from django.db.utils import IntegrityError
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
from .models import ClientSessionSymptomScore
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


@login_required
def api_handler(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            api_request = ApiRequest(data)
            api_response, status_code = do(api_request)
            return JsonResponse(api_response, status=status_code)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'error': 'Invalid JSON'}, status=400)
        except IntegrityError as err:
            return JsonResponse({'status': 'error', 'error': str(err)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'error': 'Only POST requests allowed'}, status=405)




class ApiRequest(object):

    def __init__(self, data):
        self.data = data

    @property
    def method(self):
        return self.data.get('method')

    def param(self, key):
        return self.data.get('params', {}).get(key)


def do(api_request):

    if 'set_session_symptom_score' == api_request.method:
        session_id = api_request.param('session_id')
        symptom_id = api_request.param('symptom_id')
        symptom_score = api_request.param('symptom_score')
        session = ClientSession.objects.filter(id=session_id).get()
        symptom = ClientSymptom.objects.filter(id=symptom_id).get()

        score = ClientSessionSymptomScore(session=session, symptom=symptom, score=symptom_score)
        score.save()

        return {'status': 'ok'}, 200


    if 'create_session' == api_request.method:

        client_id = api_request.param('client_id')
        
        date_string = api_request.param('date')
        format_string = "%Y-%m-%d"
        date = datetime.strptime(date_string, format_string)

        client = Client.objects.get(id=client_id)
        session = ClientSession(client=client, therapist=None, date=date)
        session.save()

        return {'status': 'ok'}, 200


    return {'status': 'error', 'error': 'Method not found'}, 404