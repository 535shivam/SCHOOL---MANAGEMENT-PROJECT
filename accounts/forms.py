from django import forms
from django.contrib.auth.models import User
from .models import Profile

class AdminUserCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email']
