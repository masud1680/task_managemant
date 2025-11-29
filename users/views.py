from django.shortcuts import render, redirect, HttpResponse,  get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User , Group
from users.forms import  CustomRegisterForm, CustomLoginForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test

from django.views.generic import FormView, TemplateView, CreateView
from django.views.generic.base import ContextMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
# create your function below.

def is_admin(user):
    return user.groups.filter(name="Admin").exists()



# Create your views here.

from django.views import View
class Gettings(View):
    messages = "I love you."

    def get(self, request):
        return HttpResponse(self.messages)
    
class MyGettings(Gettings):
    messages = "Break up to you."

# def sign_up(request):
    
#     if request.method == 'GET':
#         form = UserCreationForm()
    
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # print(form.cleaned_data)
            
    
#     return render(request, 'registration/register.html', {"form" : form})

# def sign_up(request):
    
#     if request.method == 'GET':
#         form = CustomRegisterForm()
    
#     if request.method == 'POST':
#         form = CustomRegisterForm(request.POST)
        
#         if form.is_valid():
            
#         #     username = form.cleaned_data.get('username')
#         #     password = form.cleaned_data.get('password1')
#         #     confirm_password = form.cleaned_data.get('password2')
            
#         #     if password == confirm_password:
#         #         User.objects.create(username = username, password = password)
#         #     else:
#         #         print('password are not save.')
#         # else:
#         #     print("form is invalid.")
        
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password1'))
#             # print(form.cleaned_data)
#             user.is_active = False
#             user.save()
            
#             messages.success(request,'Registration Successfull.')
#             messages.success(request,'\n\nA Confirmation mail sent. Please check your email.')
#             redirect('sign-in')
#         else:
#             messages.warning(request,'Registration Unsuccessfull.')
            
#     return render(request, 'registration/register.html', {"form" : form})


class SignUp( FormView):
    template_name = 'registration/register.html'
    form_class = CustomRegisterForm
    success_url = reverse_lazy('sign-in')


    def form_valid(self, form):

        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False
        user.save()
            
        messages.success(self.request,'Registration Successfull.')
        messages.success(self.request,'\n\nA Confirmation mail sent. Please check your email.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request,'Registration Unsuccessfull.')
        return super().form_invalid(form)
        
    

        
    


# def sign_in(request):
#     form = CustomLoginForm()
#     if request.method == 'POST':
#         form = CustomLoginForm(data = request.POST)
        
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
        
#     return render(request, 'registration/login.html', {"form" : form})
from django.core.exceptions import ImproperlyConfigured

class SignIn(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('dashboard-redirect')

    # def get_success_url(self):
        # next_url = self.request.GET.get('next')
        # return next_url if next_url else super().get_success_url()

    def get_success_url(self):
    # """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy
       

# @login_required(login_url='no-permission')
# def sign_out(request):
    
#     if request.method == 'POST':
#         logout(request)
#         return redirect('home')
    

class SignOut(LogoutView):
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

# def active_user(request, user_id, token):
#     try:
#         user = User.objects.get(id = user_id)
#         # print(user.id)
#         if default_token_generator.check_token(user, token):
#             user.is_active = True
#             # print(user.username)
#             user.save()
            
#             return  redirect('sign-in')
#         else: return HttpResponse('Invalid user or token!!')
    
#     except User.DoesNotExist:
#         return HttpResponse('User not found!!')
    

class ActiveUserView(View):

    def get(self, request, user_id, token):
        try:
            user = User.objects.get(id = user_id)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect('sign-in')
            else: return HttpResponse('Invalid user or token!!')
        except User.DoesNotExist:
            return HttpResponse('User not found!!')

    
# @user_passes_test(is_admin, login_url="no-permission")    
# def admin_dashboard(request):
#     users = User.objects.all()
#     return render(request, 'admin/dashboard.html', {"users" : users})

class AdminDashboard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = 'no-permission'
    template_name = 'admin/dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and is_admin(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context

# @user_passes_test(is_admin, login_url="no-permission")    
# def assign_role(request, user_id):
#     user = User.objects.get(id = user_id)
    
#     form = AssignRoleForm()
    
#     if request.method == 'POST':
#         form = AssignRoleForm(request.POST)
#         if form.is_valid():
#             role = form.cleaned_data.get('role')
#             user.groups.clear() # remove old roles
#             user.groups.add(role)
            
#             messages.success(request, f"User {user.username} has been assigned to the {role.name} role.")
#             return redirect('admin-dashboard')
    
#     return render(request, 'admin/assigned_role.html', {"form" : form})


@method_decorator(user_passes_test(is_admin, login_url="no-permission"), name='dispatch')
class AssignRoleView(View):
    template_name = 'admin/assigned_role.html'
    form_class = AssignRoleForm

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            role = form.cleaned_data.get('role')

            # Clear existing roles
            user.groups.clear()
            user.groups.add(role)

            messages.success(request, f"User {user.username} has been assigned to the {role.name} role.")
            return redirect('admin-dashboard')

        return render(request, self.template_name, {"form": form})

    
    
    


# @user_passes_test(is_admin, login_url="no-permission")    
# def create_group(request):
#     form = CreateGroupForm()
    
#     if request.method == 'POST':
#         form = CreateGroupForm(request.POST)
#         if form.is_valid():
#             group = form.save()
#             messages.success(request, f"Group {group.name} has been created successfully.")
#             return redirect('create-group')
#     return render(request, 'admin/create_group.html', {"form" : form})

@method_decorator(user_passes_test(is_admin, login_url="no-permission"), name='dispatch')
class CreateGroupView(FormView):
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('create-group')
    form_class = CreateGroupForm

    def form_valid(self, form):
        group = form.save()
        messages.success(self.request, f"Group {group.name} has been created successfully.")
        return super().form_valid(form)
    
    
    

# @user_passes_test(is_admin, login_url="no-permission")    
# def group_list(request):
#     groups = Group.objects.all()
    
#     return render(request, 'admin/group_list.html', {"groups" : groups})

@method_decorator(user_passes_test(is_admin, login_url="no-permission"), name='dispatch')
class GroupListView(TemplateView):
    template_name = 'admin/group_list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["groups"] = Group.objects.all()
        return self.render_to_response(context)
    

    































































































