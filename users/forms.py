from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Vote


# The forms
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    fullname = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'fullname', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['ward', 'pollingStation','stream', 'phone', 'fullname', 'id_number', 'role']
        
        

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = '__all__'