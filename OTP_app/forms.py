from socket import fromshare
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,phone_regex
from django.core.exceptions import NON_FIELD_ERRORS



def email_exists(value):
    if User.objects.filter(email=value).exists():
        raise forms.ValidationError("Profile with same email Already exists")

    

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[email_exists])
    class Meta:
        model = User
        fields = ['username','email']

class UserProfile(forms.ModelForm):

    phone_number = forms.CharField(max_length=17,validators=[phone_regex])
    class Meta:
        model = Profile
        fields = ['phone_number']