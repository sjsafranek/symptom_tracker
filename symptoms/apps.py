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

        def _alias(self):
            fn = ''
            if self.first_name:
                fn = self.first_name[0].upper()
            ln = ''
            if self.last_name:
                ln = self.last_name[0].upper()
            return '{0}{1}{2}'.format( self.id, fn, ln )
        UserModel.add_to_class('alias', _alias)
