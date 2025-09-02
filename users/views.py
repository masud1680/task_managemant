from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User , Group
from users.forms import  CustomRegisterForm, CustomLoginForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test

# create your function below.

def is_admin(user):
    return user.groups.filter(name="Admin").exists()



# Create your views here.

# def sign_up(request):
    
#     if request.method == 'GET':
#         form = UserCreationForm()
    
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # print(form.cleaned_data)
            
    
#     return render(request, 'registration/register.html', {"form" : form})

def sign_up(request):
    
    if request.method == 'GET':
        form = CustomRegisterForm()
    
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        
        if form.is_valid():
            
        #     username = form.cleaned_data.get('username')
        #     password = form.cleaned_data.get('password1')
        #     confirm_password = form.cleaned_data.get('password2')
            
        #     if password == confirm_password:
        #         User.objects.create(username = username, password = password)
        #     else:
        #         print('password are not save.')
        # else:
        #     print("form is invalid.")
        
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            # print(form.cleaned_data)
            user.is_active = False
            user.save()
            
            messages.success(request,'Registration Successfull.')
            messages.success(request,'\n\nA Confirmation mail sent. Please check your email.')
            redirect('sign-in')
        else:
            messages.warning(request,'Registration Unsuccessfull.')
            
    return render(request, 'registration/register.html', {"form" : form})


def sign_in(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        form = CustomLoginForm(data = request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        
    return render(request, 'registration/login.html', {"form" : form})

@login_required(login_url='no-permission')
def sign_out(request):
    
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
    
def active_user(request, user_id, token):
    try:
        user = User.objects.get(id = user_id)
        # print(user.id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            # print(user.username)
            user.save()
            
            return  redirect('sign-in')
        else: return HttpResponse('Invalid user or token!!')
    
    except User.DoesNotExist:
        return HttpResponse('User not found!!')
    
@user_passes_test(is_admin, login_url="no-permission")    
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {"users" : users})

@user_passes_test(is_admin, login_url="no-permission")    
def assign_role(request, user_id):
    user = User.objects.get(id = user_id)
    
    form = AssignRoleForm()
    
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # remove old roles
            user.groups.add(role)
            
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role.")
            return redirect('admin-dashboard')
    
    return render(request, 'admin/assigned_role.html', {"form" : form})

@user_passes_test(is_admin, login_url="no-permission")    
def create_group(request):
    form = CreateGroupForm()
    
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully.")
            return redirect('create-group')
    return render(request, 'admin/create_group.html', {"form" : form})

@user_passes_test(is_admin, login_url="no-permission")    
def group_list(request):
    groups = Group.objects.all()
    
    return render(request, 'admin/group_list.html', {"groups" : groups})































































































