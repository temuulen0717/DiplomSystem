from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    NEW = 'NW'
    IN_PLANNED = 'IP'
    COMPLATED = 'CMP'
    project_status_choice = [(NEW, 'New'), (IN_PLANNED, 'In planned'), (COMPLATED, 'Complated')]

    project_id = models.CharField(max_length=1000, null=True)
    category_id = models.CharField(max_length=1000, null=True)
    project_name = models.CharField(max_length=100, null=True)
    project_description = models.CharField(max_length=1000, null=True)
    project_code  = models.CharField(max_length=100, null=True)
    project_startdate = models.DateTimeField(auto_now_add=True, null=True)
   # project_enddate  = models.DateField()
    project_status = models.CharField(max_length=100, choices=project_status_choice, default=NEW)

    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE)
