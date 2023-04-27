from django.contrib import admin

# Register your models here.
from .models import Project, Book, Task, Chart

admin.site.register(Project)
admin.site.register(Book)
admin.site.register(Task)
admin.site.register(Chart)