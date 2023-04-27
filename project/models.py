from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    NEW = 'NW'
    IN_PLANNED = 'IP'
    COMPLATED = 'CMP'
    project_status_choice = [(NEW, 'New'), (IN_PLANNED, 'In planned'), (COMPLATED, 'Complated')]

    pro_id = models.AutoField(primary_key=True)
    project_id = models.CharField(max_length=1000, null=True)
    category_id = models.CharField(max_length=1000, null=True)
    project_name = models.CharField(max_length=100, null=True)
    project_description = models.TextField( null=True)
    project_code  = models.CharField(max_length=100, null=True)
   # project_startdate = models.DateField(null=True)
    #project_enddate  = models.DateField(null=True)
    project_status = models.CharField(max_length=100, choices=project_status_choice, default=NEW)

    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='users')
class Book(models.Model):

    task_name = models.CharField(max_length=100)
 
class Task(models.Model):
    NEW = 'NW'
    IN_PLANNED = 'IP'
    COMPLATED = 'CMP'
    project_status_choice = [(NEW, 'New'), (IN_PLANNED, 'In planned'), (COMPLATED, 'Complated')]

    task_name = models.CharField(max_length=100, null=True)
    task_file = models.CharField(max_length=100 ,null=True)
    task_startdate = models.DateField(null=True)
    task_enddate = models.DateField(null=True)
    task_status = models.CharField(max_length=100, choices=project_status_choice, default=NEW)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse("task", kwargs={"id": self.id})

    def get_absolute_url(self):
        return reverse("taskAdd", kwargs={"project_id": self.project_id})
    
    
class Chart(models.Model):

    name = models.CharField(max_length=1000)
    start_date = models.DateField()
    week_number = models.CharField(max_length=2, null=True)
    finish_date = models.DateField()

    responsible = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        print(self.start_date.isocalendar()[1])
        if self.week_number == "":
            self.week_number = self.start_date.isocalendar()[1]
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

