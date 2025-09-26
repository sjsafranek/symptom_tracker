from django.db.models import CharField


class LowerCaseCharField(CharField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value is not None:
            return value.lower()
        return value