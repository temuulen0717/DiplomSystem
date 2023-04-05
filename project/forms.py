# - create project 
from django import forms
from .models import Project



class CreateProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = "__all__"
        exclude = ['user',]

