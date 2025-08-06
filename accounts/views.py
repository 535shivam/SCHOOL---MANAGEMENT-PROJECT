from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import AdminUserCreationForm

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