from django import forms;
from django.contrib.auth.forms import UserCreationForm;
from django.contrib.auth.models import User;
from system import models;


class RegistForm( forms.ModelForm ):
	class Meta:
		model = models.Account;
		fields = [ "DP_account_id" ];

class LoginForm( forms.Form ):
	account_id = forms.CharField(max_length=64, required=True);
	
class AccountControlLogout( forms.Form ):
	device_id = forms.CharField(max_length=128, required=True);
	