# - create project 

from django import forms
from .models import Project

class CreateProjectForm(forms.ModelForm):
    
    class Meta:

        model = Project
        fields = ['project_name', 'project_description', 'project_code', 'project_status']
        exclude = ['user']
