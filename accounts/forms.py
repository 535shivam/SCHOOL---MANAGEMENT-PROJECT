from django import forms
from django.contrib.auth.models import User
from .models import *

class AdminUserCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email']


class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = StudentInfoModel
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Full Name.........'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'city': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your City Name.........'}),
            'pincode': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Pincode.........'})
        }


class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfoModel
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Full Name.........'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'city': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your City Name.........'}),
            'pincode': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Pincode.........'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'})        
        }