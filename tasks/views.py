from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelFrom
from tasks.models import *
from django.db.models import Q, Count, Min, Max, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView


# create your function below.

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def is_employee(user):
    return user.groups.filter(name="Employee").exists()

# Create your views here.
@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    
    type = request.GET.get('type', 'all')
    
    
    counts = Task.objects.aggregate(
        total = Count('id'), 
        completed = Count('id', filter=Q(status = "COMPLETED")),
        in_progress = Count('id', filter=Q(status = 'IN_PROGRESS')),
        pending = Count('id', filter=Q(status = 'PENDING')),
                
    )
    
    base_query = Task.objects.select_related('detail').prefetch_related('assigned_to').all()
    
    if type == 'completed':
        tasks = base_query.filter(status = 'COMPLETED')
    elif type == 'in_progress':
        tasks = base_query.filter(status = 'IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status = 'PENDING')
    elif type == 'all':
        tasks = base_query.all()
    
    context = {
        'tasks' : tasks,
        'counts' : counts,
    }
    return render(request,"dashboard/manager_dashboard.html", context)

@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    return render(request,"dashboard/users_dashboard.html")


# @login_required
# @permission_required("tasks.add_task", login_url='no-permission')
# def create_task(request):
    
#     task_form = TaskModelForm()
#     task_detail_form = TaskDetailModelFrom()
    

#     if request.method == "POST":
#         task_form = TaskModelForm(request.POST)
#         task_detail_form = TaskDetailModelFrom(request.POST, request.FILES)
#         if task_form.is_valid() and task_detail_form.is_valid():

#             '''For Django Model From Data'''
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()

#             messages.success(request, "Task Created Successfully.")
#             return redirect('create-task')
        
        
          

#     context = {"task_form" : task_form, 'task_detail_form' : task_detail_form}
#     return render(request,"task_form.html", context)


# CreateTaskDecorator = [login_required, permission_required("tasks.add_task", login_url='no-permission'),]

# @method_decorator(CreateTaskDecorator, name="dispatch")  # multipule system
# @method_decorator(login_required, name="dispatch") # single system
class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'sign-in'
    permission_required = 'tasks.add_task'
    templates = "task_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = TaskModelForm()
        context['task_detail_form'] = TaskDetailModelFrom()

        return context
    
    def get(self, request, *args, **kwargs):
        

        context = self.get_context_data()
        return render(request, self.templates, context)
    
    def post(self, request, *args, **kwargs):
        
        if request.method == "POST":
            task_form = TaskModelForm(request.POST)
            task_detail_form = TaskDetailModelFrom(request.POST, request.FILES)
            if task_form.is_valid() and task_detail_form.is_valid():

                '''For Django Model From Data'''
                task = task_form.save()
                task_detail = task_detail_form.save(commit=False)
                task_detail.task = task
                task_detail.save()

                messages.success(request, "Task Created Successfully.")
                return redirect('create-task')
    

@login_required
@permission_required("tasks.change_task", login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance= task)
    
    if task.detail:
        task_detail_form = TaskDetailModelFrom(instance= task.detail)
    

    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance= task)
        task_detail_form = TaskDetailModelFrom(request.POST, instance= task.detail)
        if task_form.is_valid() and task_detail_form.is_valid():

            '''For Django Model From Data'''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully.")
            return redirect('update-task', id)
        
        
    context = {"task_form" : task_form, 'task_detail_form' : task_detail_form}
    return render(request,"task_form.html", context)

@login_required
@permission_required("tasks.delete_task", login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Deleted Successfully.")
        return redirect('manager-dashboard')
    else:
        messages.success(request, "Something went wrong!!")
        return redirect('manager-dashboard')
    
# @login_required
# @permission_required("projects.view_project", login_url='no-permission')
# def view_project(request):
#     # tasks = TaskDetail.objects.exclude(priority = "L") #problume
#     projects = Project.objects.annotate(
#         num_task =Count('task')
#     ).order_by('num_task')
    
#     return render(request, 'dashboard/view_projects.html', {'projects' : projects})

viewProjectsDecorator = [login_required, permission_required('projects.view_project', login_url='no-permission')]
@method_decorator(viewProjectsDecorator, name="dispatch")
class ViewProjects(ListView):
    model = Project
    context_object_name = "projects"
    template_name = "dashboard/view_projects.html"

    def get_queryset(self):
        queryset = Project.objects.annotate(
        num_task =Count('task')).order_by('num_task')
        
        return queryset
    

    

# @login_required
# @permission_required("tasks.view_task", login_url='no-permission')
# def task_details(request, task_id):
#     task = Task.objects.get(id = task_id)
#     status_choices = Task.STATUS_CHOICES
    
#     if request.method == 'POST':
#         selece_status = request.POST.get('task_status')
#         task.status = selece_status
#         task.save()
#         return redirect('task-details', task.id)
    
#     return render(request, 'task_details.html', {"task" : task, "status_choices" : status_choices})

class TaskDetails(DetailView):
    model = Task
    template_name ='task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES

        return context
    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        select_status = request.POST.get('task_status')
        task.status = select_status
        task.save()
        return redirect('task-details', task.id )

@login_required
def deshboard_redirect(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return redirect('no-permission')