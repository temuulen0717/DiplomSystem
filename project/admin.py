from django.contrib import admin

# Register your models here.
from .models import Project, Book

admin.site.register(Project)
admin.site.register(Book)