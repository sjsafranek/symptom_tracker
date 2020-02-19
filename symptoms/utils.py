from django.contrib.auth.models import User

def getUserByUsername(username):
    return User.objects.filter(username=username).first()
