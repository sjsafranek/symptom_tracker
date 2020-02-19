from django.apps import AppConfig
from django.contrib.auth import get_user_model


class SymptomsConfig(AppConfig):
    name = 'symptoms'

    def ready(self):
        # extend to user model
        UserModel = get_user_model()

        def _isClient(self):
            return None != self.client
        UserModel.add_to_class('isClient', _isClient)

        def _isTherapist(self):
            return None != self.therapist
        UserModel.add_to_class('isTherapist', _isTherapist)
