from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelFrom
from tasks.models import *
from django.db.models import Q, Count, Min, Max, Avg
from django.contrib import messages

#signals import
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_delete
from django.core.mail import send_mail

# Create your views here.

def manager_dashboard(request):
    
    type = request.GET.get('type', 'all')
    
    
    #getting task count
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status = "COMPLETED").count()
    # in_progress_task = Task.objects.filter(status = "IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status = "PENDING").count()
    
    # context = {
    #     'tasks' : tasks,
    #     'total_task' : total_task,
    #     'completed_task' : completed_task,
    #     'in_progress_task' : in_progress_task,
    #     'pending_task' : pending_task,
    # }
    
    
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

def users_dashboard(request):
    return render(request,"dashboard/users_dashboard.html")

def test(request):
    context = {
        "name" : ["Akash","Abeg","Masud"],
        "age" : [18],
    }
    return render(request,"test.html",context)

# def create_task(request):
#     # using for get post learning
#     return render(request,"task_form.html")

def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelFrom()
    

    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelFrom(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():

            '''For Django Model From Data'''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully.")
            return redirect('create-task')
        
        
            ''' For Django From Data'''
            # data = form.cleaned_data
            # title = data.get("title")
            # description = data.get("description")
            # due_date = data.get("due_date")
            # assigned_to = data.get("assigned_to") # list [1,3]

            # Task = task.objects.create(
            #     title = title, description = description , due_date = due_date
            # )

            # #assigned employee to task
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id = emp_id)
            #     Task.assigned_to.add(employee)
            
            # return HttpResponse("Task Added Successfully")

    context = {"task_form" : task_form, 'task_detail_form' : task_detail_form}
    return render(request,"task_form.html", context)

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

def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Deleted Successfully.")
        return redirect('manager-dashboard')
    else:
        messages.success(request, "Something went wrong!!")
        return redirect('manager-dashboard')

def view_task(request):
    # tasks = Task.objects.all()
    # tasks = Task.objects.filter(status = 'PENDING')
    tasks = TaskDetail.objects.exclude(priority = "L") #problume
     
    return render(request, 'dashboard/view_task.html', {'tasks' : tasks})



# email send when task assigned to some person

@receiver(m2m_changed, sender= Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        print(instance, instance.assigned_to.all())
        
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        print('chaking.......', assigned_emails)
        
        send_mail(
            "New Task Assigned",
            f'You have been assigned to the task: {instance.title}',
            "masudhasan1680@gmail.com",
            assigned_emails,
            fail_silently=False
        )
        
        

# delete task-detail model when task deleted using signals

@receiver(post_delete, sender= Task)
def delete_associate_details(sender, instance, **kwargs):
    
    if instance.detail:
        print(isinstance)
        
        instance.detail.delete()
        
        print("Deleted Successfully. ")
