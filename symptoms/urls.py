from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('dashboard/client/<int:client_id>', views.client_dashboard, name="dashboard"),
    path('api/v1/therapist/<int:therapist_id>/clients', views.get_clients_by_therapist, name="get_clients_by_therapist"),
    path('api/v1/client/<int:client_id>/sessions', views.get_sessions_by_client, name="get_sessions_by_client"),
    path('api/v1/client/<int:client_id>/symptoms', views.get_symptoms_by_client, name="get_symptoms_by_client"),
    path('api/v1/session/<int:session_id>/protocol', views.get_protocol_by_session, name="get_protocol_by_session"),
    path('api/v1', views.api_handler, name="api_handler")
]
