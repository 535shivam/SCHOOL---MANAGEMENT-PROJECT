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
        fields = ["username", "email"]


class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = StudentInfoModel
        fields = "__all__"
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Your Full Name.........",
                }
            ),
            "dob": forms.DateInput(attrs={"type": "date"}),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Your City Name.........",
                }
            ),
            "pincode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Your Pincode.........",
                }
            ),
        }


class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfoModel
        fields = "__all__"
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Your Full Name.........",
                }
            ),
            "dob": forms.DateInput(attrs={"type": "date"}),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Your City Name.........",
                }
            ),
            "pincode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Your Pincode.........",
                }
            ),
            "language": forms.Select(attrs={"class": "form-control"}),
            "subject": forms.Select(attrs={"class": "form-control"}),
        }


# Add class room titmetable
class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoomModel
        fields = ["teacher", "class_name", "subject"]


class StudentMarksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        student_class = kwargs.pop("student_class", None)
        super(StudentMarksForm, self).__init__(*args, **kwargs)

        if student_class and student_class <= 10:
            for field in ["subject7", "subject8", "subject9"]:
                if field in self.fields:
                    self.fields[field].widget = forms.HiddenInput()
                    self.fields[field].required = False

    class Meta:
        model = StudentMarksModel
        exclude = ["total_marks", "percentage", "division"]


# student Notice Form
class StudentNoticeForm(forms.ModelForm):
    class Meta:
        model = StudentNoticeModel
        fields = ["student", "title", "message", "upload"]


# General Notice for all user
class GeneralNoticeForm(forms.ModelForm):
    class Meta:
        model = GeneralNoticeModel
        fields = ["title", "message", "upload"]


# Assignment by teacher
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = AssignmentModel
        fields = ["class_name", "title", "description", "attachment", "due_date"]
