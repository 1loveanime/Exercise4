from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import PersonDetail

class RegistrationForm(UserCreationForm):
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class PersonAddForm(ModelForm):
	
	class Meta:
		model = PersonDetail
		exclude = ('user', 'profilepicture', )
		