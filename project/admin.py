from django.contrib import admin

# Register your models here.
from .models import Project, Book, Task

admin.site.register(Project)
admin.site.register(Book)
admin.site.register(Task)