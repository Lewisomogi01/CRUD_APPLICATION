from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm
from .models import Record

def home(request):
    return render(request, 'webapp/index.html')

# Register
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the desired page after registration
            return redirect('dashboard')
            
    context = {'form': form}
    return render(request, 'webapp/register.html', context=context)

# Login user
def my_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the dashboard after login
                return redirect('dashboard')

    context = {'form': form}
    return render(request, 'webapp/login.html', context=context)

# Dashboard
@login_required(login_url='login')
def dashboard(request):
    
    
    my_records = Record.objects.all()
    
    
    context = {'records' : my_records}
    
    return render(request, 'webapp/dashboard.html', context=context)

# Logout
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")

       