from django import forms
from tasks.models import Task

# Django form
class TaskForm(forms.Form):
    title = forms.CharField( max_length=250, label = "Task Title")
    description = forms.CharField(widget = forms.Textarea, label = "Task Description ")
    due_date = forms.DateField(widget = forms.SelectDateWidget, label = "Due Date")
    assigned_to = forms.MultipleChoiceField( widget = forms.CheckboxSelectMultiple, choices = [])
    def __init__(self, *args, **kwargs):
        # print(args, kwargs)
        employees = kwargs.pop("employees", [])

        # print("pop  korar pore" , args, kwargs)
        # print(employees)
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [
            (emp.id, emp.name) for emp in employees
        ]
        
# Django Model form

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        # fields = '__all__' #Select all fields
        fields = ['title', 'description', 'due_date', 'assigned_to'] # Select some custom fields
        # exclude = ['project', 'is_completed', 'created_at','updated_at'] # unshow this fields

        widgets ={
     
            'due_date' : forms.SelectDateWidget,
            'assigned_to' : forms.CheckboxSelectMultiple
        }
