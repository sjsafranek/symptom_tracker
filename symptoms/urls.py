from django.urls import path

from . import views

print(dir(views))

urlpatterns = [
    path('', views.index, name='index'),
]
