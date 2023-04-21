"""ProjectManageSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from project import views
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', include('project.urls')), 
    path('admin/', admin.site.urls),
    path("home/", views.home, name='home'), 
    path('createProject/', views.createProject, name='createProject'),
    path('signup/', views.register, name="register"), 
    path('login/', views.LoginPage, name="login"), 
    path('logout/', views.Logout, name='logout'),
    path('viewProject/', views.viewProject, name='viewProject' ),
    path('updateProject/<str:pk>/', views.updateProject, name="updateProject"),
    path('deleteProject/<str:pk>/', views.deleteProject, name='deleteProject'),
    path('task/<str:id>', views.taskView, name='task'),
    path('addTask/', views.addTask, name='addTask'),
    path('editTask/', views.editTask, name='editTask'),
    path('updateTask/<str:id>', views.updateTask, name='updateTask'),
    path('deleteTask/<str:id>', views.deleteTask, name='deleteTask'), 
]