from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from .models import *
from .forms import *
import re

# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                role = user.profile.role  # 👈 this line is safe now
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found. Contact admin.")
                return redirect('login')

            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'teacher':
                return redirect('teacher_dashboard')
            elif role == 'student':
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


# ADMIN DASHBOARD
@login_required
def admin_dashboard(request):
    if request.user.profile.role != 'admin':
        return redirect('unauthorized')

    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = name
            user.save()
            # Profile.objects.create(user=user, role=role, mobile=mobile)
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.mobile = mobile
            profile.save()

            messages.success(request, f"{role.title()} added successfully!")
            return redirect('admin_dashboard')
    else:
        form = AdminUserCreationForm()
    return render(request, 'admin_dashboard.html', {'form': form})


@login_required
def teacher_dashboard(request):
    if request.user.profile.role != 'teacher':
        return redirect('unauthorized')
    return render(request, 'teacher_dashboard.html')


@login_required
def student_dashboard(request):
    if request.user.profile.role != 'student':
        return redirect('unauthorized')
    return render(request, 'student_dashboard.html')


def unauthorized_view(request):
    return render(request, 'unauthorized.html')


def logout_view(request):
    logout(request)
    return redirect('login')



# Student View
@login_required
def student_info_view(request):
    if request.user.profile.role != 'student':
        return redirect('unauthorized')
    
    student_info = getattr(request.user, 'studentinfomodel', None)


    if request.method == 'POST':
        form = StudentInfoForm(request.POST , instance=student_info)
        if form.is_valid():
            student_info = form.save(commit=False)
            student_info.user = request.user
            student_info.save()
            messages.success(request,'Information saved successfully!')
            return redirect('student_info')
    else:
        form = StudentInfoForm(instance=student_info)

    return render(request,'student_info.html',{'form':form})


# Teacher View
@login_required
def teacher_info_view(request):
    if request.user.profile.role != 'teacher':
        return redirect('unauthorized')
    
    teacher_info = getattr(request.user, 'teacherinfomodel', None)


    if request.method == 'POST':
        form = TeacherInfoForm(request.POST , instance=teacher_info)
        if form.is_valid():
            teacher_info = form.save(commit=False)
            teacher_info.user = request.user
            teacher_info.save()
            messages.success(request,'Information saved successfully!')
            return redirect('teacher_info')
    else:
        form = TeacherInfoForm(instance=teacher_info)

    return render(request,'teacher_info.html',{'form':form})


@login_required
def teacher_timetable_view(request):
    if request.user.profile.role != 'teacher':
        return HttpResponse("Unauthorized", status=403)

    try:
        teacher_info = TeacherInfoModel.objects.get(user=request.user)
    except TeacherInfoModel.DoesNotExist:
        return HttpResponse("Teacher profile not found.")

    classes = ClassRoomModel.objects.filter(teacher=teacher_info)
    return render(request, 'teacher_timetable.html', {'classes': classes})


# class add
@login_required
def class_add_view(request):
    if request.user.profile.role != 'admin':
        return HttpResponse("Unauthorized", status=403)

    if request.method == 'POST':
        form = ClassRoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class added.")
            return redirect('class_list')
    else:
        form = ClassRoomForm()

    return render(request, 'class_add.html', {'form': form})


# create class
@login_required
def class_list_view(request):
    if request.user.profile.role != 'admin':
        return HttpResponse("Unauthorized", status=403)

    classes = ClassRoomModel.objects.all()
    return render(request, 'class_list.html', {'classes': classes})



# marks Entry by teacher
@login_required
def add_student_marks(request):
    if request.user.profile.role != 'teacher':
        return HttpResponse("Unauthorized", status=403)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        try:
            student = User.objects.get(id=student_id)
        except User.DoesNotExist:
            messages.error(request, "Student not found.")
            return redirect('add_marks')

        # Get existing entry if any
        existing = StudentMarksModel.objects.filter(student=student).first()

        # Bind form to existing or new
        form = StudentMarksForm(request.POST, instance=existing)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.student = student 
            obj.save() 
            messages.success(request, "Marks saved successfully.")
            return redirect('add_marks')
    else:
        form = StudentMarksForm()

    return render(request, 'add_marks.html', {'form': form})


# student result
@login_required
def student_marks_view(request):
    if request.user.profile.role != 'student':
        return HttpResponse("Unauthorized", status=403)

    try:
        marks = StudentMarksModel.objects.get(student=request.user)
    except StudentMarksModel.DoesNotExist:
        marks = None

    return render(request, 'student_marks.html', {'marks': marks})


# Teacher send notice
@login_required
def send_notice_view(request):
    if request.user.profile.role != 'teacher':
        return HttpResponse("Unauthorized", status=403)

    if request.method == 'POST':
        form = StudentNoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.teacher = request.user
            notice.save()
            messages.success(request, "Notice sent successfully.")
            return redirect('send_notice')
    else:
        form = StudentNoticeForm()

    return render(request, 'send_notice.html', {'form': form})


#student see notice
@login_required
def student_notices_view(request):
    if request.user.profile.role != 'student':
        return HttpResponse("Unauthorized", status=403)

    notices = request.user.notices_received.all().order_by('-created_at')
    return render(request, 'student_notices.html', {'notices': notices})


#admin send general notice
@login_required
def send_general_notice(request):
    if request.user.profile.role != 'admin':
        return HttpResponse("Unauthorized", status=403)

    if request.method == 'POST':
        form = GeneralNoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.sender = request.user
            notice.save()
            messages.success(request, "General notice sent successfully.")
            return redirect('send_general_notice')
    else:
        form = GeneralNoticeForm()

    return render(request, 'send_general_notice.html', {'form': form})



#user see all genaral notice
@login_required
def general_notices_view(request):
    notices = GeneralNoticeModel.objects.all().order_by('-created_at')
    return render(request, 'general_notices.html', {'notices': notices})


#take attendance
@login_required
def take_attendance_view(request):
    if request.user.profile.role != 'teacher':
        return HttpResponse("Unauthorized", status=403)

    teacher_info = TeacherInfoModel.objects.get(user=request.user)
    classes = ClassRoomModel.objects.filter(teacher=teacher_info)

    raw_class = request.GET.get('class') or request.POST.get('class_name')
    selected_class = re.sub(r'\D', '', raw_class) if raw_class else None

    students = []
    if selected_class:
        students = StudentInfoModel.objects.filter(studentclass=selected_class)
        print("Selected class:", selected_class)
        print("Students found:", students.count())

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            AttendanceModel.objects.create(
                teacher=request.user,
                class_name=selected_class,
                student=student.user,
                status=status,
                date=timezone.now().date()
            )
        messages.success(request, "Attendance submitted successfully.")
        return redirect('take_attendance')

    return render(request, 'take_attendance.html', {
        'classes': classes,
        'students': students,
        'selected_class': raw_class
    })
