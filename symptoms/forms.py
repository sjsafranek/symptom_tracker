from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Profile
from .models import UserPhone
# from .enums import Pronouns
# from .enums import PhoneType


def makeDateInput():
	return forms.DateInput(
		attrs = {
			"class": "form-control form-control-sm", 
			"placeholder": "Select a date",
			"type": "date"
		}
	)

def makeTextInput():
	return forms.TextInput(
		attrs = {
			"class": "form-control form-control-sm"
		}
	)

def makeTelephoneInput():
	return forms.TextInput(
		attrs = {
			"class": "form-control form-control-sm",
			"type": "tel"
		}
	)

def makeSelect():
	return forms.Select(
		attrs = {
			"class": "form-control form-control-sm"
		}
	)

def makeTextArea():
	return forms.Textarea(
		attrs = {
			"class": "form-control form-control-sm"
		}
	)



class ProfileForm(ModelForm):
	birth_date = forms.DateField(required=False, widget=makeDateInput())
	bio = forms.CharField(label="About Me", required=False, widget=makeTextArea())
	pronouns = forms.ChoiceField(required=False, choices=Pronouns.choices, widget=makeSelect())
	picture = forms.ImageField(label="Profile Picture", required=False, widget=forms.FileInput(attrs={"class": "form-control-file form-control-sm"}))

	class Meta:
		model = Profile
		fields = [
			'bio', 
			'birth_date',
			'pronouns',
			'picture'
		]



class PhoneForm(ModelForm):
	user = forms.ModelChoiceField(
		# widget=forms.HiddenInput(),
		queryset = User.objects.filter(is_active=True),
		initial = lambda: self.initial.get('user') or self.request.user,
	)
	phone_number = forms.CharField(required=True, widget=makeTelephoneInput())
	phone_type = forms.ChoiceField(required=False, choices=PhoneType.choices, widget=makeSelect())
	is_preferred = forms.BooleanField(required=False)

	class Meta:
		model = UserPhone
		fields = [
			'user',
			'phone_number',
			'phone_type',
			'is_preferred'
		]
