from django.contrib import messages
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import CreateProjectForm, TaskForm, InviteUserForm
from .models import Project, Task, Chart, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import pandas as pd
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from dash import html
import dash
from django.db.models import Q



# Create your views here.
@login_required(login_url='login') 
def home(request):
    return render(request, 'home.html')

def home_view(request):
    return render(request, 'index.html')

#create project
@login_required(login_url='login') 
def createProject(request):

    form = CreateProjectForm()
 
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)

        if form.is_valid():
            
            project = form.save(commit=False)
            project.user = request.user
            project.save()

            return redirect('viewProject')
        
    context = {'form':form}
    return render(request, 'project.html', context=context)


# view project
@login_required(login_url='login') 
def viewProject(request):
      
      current_user = request.user.id
      project = Project.objects.all().filter(user=current_user)
      if 'q' in request.GET:
          q = request.GET['q']
          project = Project.objects.filter(Q(project_name = q))
      context = {'project': project}

      return render(request, 'view-project.html', context=context)


# update project
@login_required(login_url='login')
def updateProject(request, pk):

      project = Project.objects.get(pro_id=pk)

      form = CreateProjectForm(instance=project)

      if request.method == 'POST':
          form = CreateProjectForm(request.POST, instance=project)

          if form.is_valid():
              
              form.save()
              messages.success(request, "Амжилттай шинчлэгдлээ")
              return redirect('viewProject')

      context = {'form':form}

      return render(request, 'update-project.html', context=context)

# delete project 

login_required(login_url='login')
def deleteProject(request, pk):
    
    project = Project.objects.get(pro_id=pk)

    if request.method == 'POST':
        project.delete()

        return redirect('viewProject')

    return render(request, 'delete-project.html')


#register
def register(request):   
  if request.method =='POST':  
      uname=request.POST.get('username') 
      email=request.POST.get('email') 
      pass1=request.POST.get('password1')    
      pass2=request.POST.get('password2')  

      if pass1!=pass2: 
        return HttpResponse("Нууц үг зөрүүтэй байна!!!") 
      else: 
        my_user=User.objects.create_user(uname,email,pass1) 
        my_user.save() 
        return redirect('login')
  return render(request, 'signup.html')


#login
def LoginPage(request):  
  if request.method=='POST': 
      username=request.POST.get('username') 
      pass1=request.POST.get('pass') 
      user=authenticate(request, username=username, password=pass1) 
      if user is not None: 
          login(request, user) 
          return redirect('home') 
      else:  
          messages.error(request, "Нэвтрэх нэр, нууц үг буруу байна")


  return render(request, 'login.html')  


#logout
def Logout(request): 
  logout(request) 
  return redirect('login')


  #task
def taskView(request, id):
    proj = Project.objects.get(pro_id = id)
    tasks = Task.objects.filter(project = proj)
    context = {'cat': proj, 'task': tasks }
    return render(request, 'task/task.html', context=context)

#add task 
def addTask(request, id):
    project = Project.objects.get(pro_id=id)
    if request.method == "POST":
        task_name = request.POST.get('task_name')
        task_startdate = request.POST.get('task_startdate')
        task_enddate = request.POST.get('task_enddate')
        task_status = request.POST.get('task_status')
        task_file = request.POST.get('task_file')
            
        task = Task(
            task_name = task_name,
            task_startdate = task_startdate,
            task_enddate = task_enddate,
            task_status = task_status,
            task_file = task_file 
        )
        task.project = project
        task.save()
        return redirect(reverse('project', args=[id]))

    return render(request, 'task/task.html')



#edit task 

def editTask(request):
    task = Task.objects.all()

    context = {
        'task': task,
    }

    return render(request, 'task/task.html', context)

#update task

def updateTask(request, id):

    if request.method == "POST":
        task_name = request.POST.get('task_name')
        task_startdate = request.POST.get('task_startdate')
        task_enddate = request.POST.get('task_enddate')
        task_status = request.POST.get('task_status')
        task_file = request.POST.get('task_file')

        task = Task(
            id = id,
            task_name = task_name,
            task_startdate = task_startdate,
            task_enddate = task_enddate,
            task_status = task_status,
            task_file = task_file 
        )
        task.save()
        return redirect('project')

    return redirect(request, 'task/task.html')


#delete Task
def deleteTask(request, id):
    
    task = Task.objects.filter(id = id) 
    
    context = {
        'task': task,
    }

    task.delete()
    return redirect('project')


#addTask test ---------------

def taskAdd(request, project_id):
    project = Project.objects.get(pro_id = project_id)
    fform = TaskForm()
 
    if request.method == 'POST':
        fform = TaskForm(request.POST)

        if fform.is_valid():
            
            task = fform.save(commit=False)
            task.project = project
            task.save()

            return redirect(reverse('project', project_id=project.pro_id))
        
    context = {'fform':fform}
    return render(request, 'task/addTask.html', context=context)



def Charts(request, id):
    proj = Project.objects.get(pro_id = id)
    tasks = Task.objects.filter(project = proj)
    fig = go.Figure(data=go.Scatter(x=[1, 3, 2], y=[4,5,6]))
    projects_data = [
        {
            'Project': x.task_name,
            'Start': x.task_startdate,
            'Finish': x.task_enddate,
            'Task': x.task_name
        } for x in tasks
    ]
    df = pd.DataFrame(projects_data)
    fig = px.timeline(
        df, x_start="Start", x_end="Finish", y="Project", color="Task", width=1000, height=400
    )
    fig.update_layout(
        margin=dict(l=200, t=100, b=20),
        yaxis=dict(showgrid=True),
        xaxis=dict(showgrid=False),

    )
    fig.update_yaxes(autorange="reversed")
    fig.update_traces(width=0.2)
    gantt_plot = plot(fig, output_type="div")
    context = {'plot_div': gantt_plot, 'task': tasks }
    return render(request, 'gantt/index.html', context)



#invite user ----------------
def invite_user(request, project_id):
    project = Project.objects.get(pro_id=project_id)
    if request.method == 'POST':
        form = InviteUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # create a new user account if the email address is not associated with an existing account
                user = User.objects.create_user(email, email)
                user.save()
                profile = UserProfile(user=user)
                profile.save()
            project.users.add(user)
            return redirect('project', project_id=project.pro_id)
    else:
        form = InviteUserForm()
    return render(request, 'invite_user.html', {'form': form, 'project': project})

