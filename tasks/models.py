from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings

# Create your models here.


class Task(models.Model):
    
    STATUS_CHOICES = [
         ('PENDING', 'Pending'),
         ('IN_PROGRESS', 'In Progress'),
         ('COMPLETED', 'Completed'),
     ]
    project = models.ForeignKey(
         'Project', 
         on_delete = models.CASCADE,
         default = 1
         )
    # assigned_to = models.ManyToManyField(Employee, related_name="task")
    assigned_to = models.ManyToManyField(User, related_name="task")
     
    title = models.CharField(max_length=251)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices= STATUS_CHOICES, default='PENDING')
    is_completed = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title
    
    

# one to one 
# many to one 
# many to many 

class TaskDetail(models.Model):
    HIGH = 'H'
    NORMAL = 'N'
    LOW = 'L'

    # Create a options using tuppol
    PRIORITY_OPTIONS = (
        (HIGH,'HIGH'),
        (NORMAL,'NORMAL'),
        (LOW,'LOW')
    )
    # One to One Relation
    task = models.OneToOneField(Task,
    #  on_delete = models.CASCADE,
    on_delete= models.DO_NOTHING
     , related_name='detail')

    asset = models.ImageField(upload_to='task_asset',  blank=True, null=True, default='task_asset/default_img.jpg')
    priority = models.CharField(max_length = 1, choices = PRIORITY_OPTIONS, default = LOW)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Fetails form Task {self.task.title}"

class Project(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    
    def __str__(self):
        return self.name












