from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import *

# Create your views here.

def manager_dashboard(request):
    return render(request,"dashboard/manager_dashboard.html")

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
    form = TaskModelForm()

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():

            '''For Django Model From Data'''
            form.save()

            return render(request,'task_form.html', {"form":form, "message":'Task Added Successfully'})
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

    context = {"form" : form}
    return render(request,"task_form.html", context)



def view_task(request):
    # tasks = Task.objects.all()
    # tasks = Task.objects.filter(status = 'PENDING')
    tasks = TaskDetail.objects.exclude(priority = "L") #problume
     
    return render(request, 'dashboard/view_task.html', {'tasks' : tasks})
