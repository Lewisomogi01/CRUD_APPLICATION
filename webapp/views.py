from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from .models import Record

from django.contrib import messages

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
            messages.success(request, "Account created successfully!")
            
            return redirect('login')
            
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
                messages.success(request, "You have logged in successfully!!")
            
                
                return redirect('dashboard')

    context = {'form': form}
    return render(request, 'webapp/login.html', context=context)

# Dashboard
@login_required(login_url='login')
def dashboard(request):
    
    
    my_records = Record.objects.all()
    
    
    context = {'records' : my_records}
    
    return render(request, 'webapp/dashboard.html', context=context)

#--create or add record
@login_required(login_url='login')
def create_record(request):
    
    form = CreateRecordForm()
    
    if request.method == "POST":
        
        form = CreateRecordForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            
            messages.success(request, "Record was created successfully!")
            
            
            return redirect("dashboard")
        
    context = {'form': form}
    
    return render(request,'webapp/create-record.html', context=context)
    
#update record
@login_required(login_url='login')
def update_record(request,pk):
    
    record= Record.objects.get(id=pk)
    
    form= UpdateRecordForm(instance=record)
    
    if request.method== "POST":
        
        form = UpdateRecordForm(request.POST, instance=record)
        
        if form.is_valid():
            
            form.save()
            
            messages.success(request, "Your record was updated successfully!")
            
            
            return redirect("dashboard")
    context = {'form': form}
    
    return render(request, 'webapp/update-record.html', context=context)
       
    
#read or view a single record

@login_required(login_url='login')
def singular_record (request,pk):
    
    all_records = Record.objects.get(id=pk)
    
    context = {'record':all_records}
    
    return render(request, 'webapp/view-record.html', context)

#delete a record

@login_required(login_url='login')
def delete_record (request,pk):
    
    record = Record.objects.get(id=pk)
    
    record.delete()
    
    messages.success(request, "Your record was deleted successfully!")
            
    
    return redirect ("dashboard")
    
# Logout
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        
        messages.success(request, "You logged out successfully!")
            
    return redirect("login")

       