from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Department, CustomUser

def home(request):
    return render(request, 'users/home.html')  

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard' if user.is_admin else 'user_dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('user_dashboard')
    users = CustomUser.objects.all()
    return render(request, 'users/admin_dashboard.html', {'users': users})

@login_required
def user_dashboard(request):
    if request.user.department:
        files = request.user.department.departmentfile_set.all()
    else:
        files = []
    return render(request, 'users/user_dashboard.html', {'files': files})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_user(request):
    if not request.user.is_admin:
        return redirect('user_dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/create_user.html', {'form': form})

