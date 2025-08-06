from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.role}"



#Student info Model
class StudentInfoModel(models.Model):
    classChoice = {
        ('','SELECT'),
        ('1','Class 1'),
        ('2','Class 2'),
        ('3','Class 3'),
        ('4','Class 4'),
        ('5','Class 5'),
        ('6','Class 6'),
        ('7','Class 7'),
        ('8','Class 8'),
        ('9','Class 9'),
        ('10','Class 10'),
        ('11','Class 11'),
        ('12','Class 12')
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    studentclass =  models.CharField(max_length=10,choices=classChoice,default='SELECT')

    def __str__(self):
        return self.full_name
    

# Teacher Info Model
class TeacherInfoModel(models.Model):
    langChoice = {
        ('' , 'SELECT'),
        ('Hindi' , 'Hindi'),
        ('English' , 'English')
    }
    subjectChoice = {
        ('' , 'SELECT'),
        ('Hindi' , 'Hindi'),
        ('English' , 'English'),
        ('Physics' , 'Physics'),
        ('Chemistry' , 'Chemistry'),
        ('Biology' , 'Biology'),
        ('Computer' , 'Computer'),
        ('Maths' , 'Maths'),
        ('Arts' , 'Arts'),
        ('Social Science' , 'Social Science'),
        ('Sanskrit' , 'Sanskrit')
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    subject =  models.CharField(max_length=100 , choices=subjectChoice , default='')
    language = models.CharField(max_length=50 , choices=langChoice , default='')

    def __str__(self):
        return self.full_name
    

#Time Table
class ClassRoomModel(models.Model):
    teacher = models.ForeignKey(TeacherInfoModel, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.class_name} - {self.subject}"