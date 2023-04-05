from django.contrib import messages
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import CreateProjectForm
from .models import Project
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
      
      context = {'project': project}

      return render(request, 'view-project.html', context=context)


# update project
@login_required(login_url='login')
def updateProject(request, pk):

      project = Project.objects.get(id=pk)

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
    
    project = Project.objects.get(id=pk)

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