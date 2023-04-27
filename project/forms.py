# - create project 
from django import forms
from .models import Project, Task



class CreateProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = "__all__"
        exclude = ['user',]

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = "__all__"
        exclude = ['project']

class InviteUserForm(forms.Form):

    email = forms.EmailField()