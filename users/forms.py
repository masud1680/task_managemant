from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group, Permission
from django import forms
import re
from tasks.forms import StyledFormMixin

# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
#     def __init__(self, *args, **kwargs):
#         super(UserCreationForm, self).__init__(*args, **kwargs)
        
#         for fieldsname in ['username', 'password1', 'password2']:
#             self.fields[fieldsname].help_text = None
            
class CustomRegisterForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget= forms.PasswordInput)
    confirm_password = forms.CharField(widget= forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'confirm_password', 'email']
    
        
    def clean_password1(self):
        
        password1 = self.cleaned_data.get('password1')
        
        errors = []
        if len(password1) < 8:
            errors.append('Passwrod must be at least 9 charecter long')
    
        # if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password1):
        #     # match
        #     errors.append('Password must input Uppercase, lowercase, number & special charecters')
        
        # if "abc" not in password1:
        #     errors.append('Password must have abc')
        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email = email).exists()
        
        if email_exists:
            raise forms.ValidationError('Email already exists.')
        
        return email
            

    def clean(self): # non-field
        cleaned_data = super().clean()
        
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError('Password do not match.')
        
        return cleaned_data
        
        
        
        
class CustomLoginForm(StyledFormMixin, AuthenticationForm):
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label= "Select a Role"
    )
      
class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget =forms.CheckboxSelectMultiple,
        required= False,
        label = "Assign Permission"
    )      
    
    class Meta:
        model = Group
        fields=['name', 'permissions']