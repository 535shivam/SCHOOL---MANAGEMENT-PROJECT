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
    

class StudentMarksModel(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'student'})
    subject1 = models.IntegerField()
    subject2 = models.IntegerField()
    subject3 = models.IntegerField()
    subject4 = models.IntegerField()
    subject5 = models.IntegerField()
    subject6 = models.IntegerField()
    subject7 = models.IntegerField()
    subject8 = models.IntegerField()
    subject9 = models.IntegerField()
    subject10 = models.IntegerField()
    total_marks = models.IntegerField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    division = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        total = (
            self.subject1 + self.subject2 + self.subject3 + self.subject4 + self.subject5 +
            self.subject6 + self.subject7 + self.subject8 + self.subject9 + self.subject10
        )
        percent = total / 10
        self.total_marks = total
        self.percentage = percent

        if percent >= 65:
            self.division = 'First Division'
        elif percent > 50:
            self.division = 'Second Division'
        elif percent > 35:
            self.division = 'Third Division'
        else:
            self.division = 'Fail'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.percentage:.2f}%"


#student notice model
class StudentNoticeModel(models.Model):
    teacher = models.ForeignKey(User , on_delete=models.CASCADE , limit_choices_to={'profile__role': 'teacher'} , related_name='notices_sent')
    student = models.ForeignKey(User , on_delete=models.CASCADE , limit_choices_to={'profile__role': 'student'} , related_name='notices_received')
    title = models.CharField(max_length=100)
    message = models.TextField()
    upload = models.FileField(upload_to='student_notes/' ,blank=True , null= True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} → {self.student.username}"
    

# common msg by admin
class GeneralNoticeModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE , limit_choices_to={'profile__role': 'admin'})
    title = models.CharField(max_length=100)
    message = models.TextField()
    upload = models.FileField(upload_to='general_notices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title