from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def home(request):
    return render(request,'home.html')

def sign_up(request):
    if request.method == 'GET':
       return render(request,'signup.html', {'form': UserCreationForm})

    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST["username"],password = request.POST["password1"])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(request,'signup.html',{"form":UserCreationForm,"error":"Username already exists"})
        
        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

def log_in(request,):
    if request.method == 'GET':
        return render(request,'login.html',{"form":AuthenticationForm})
    
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])

        if user is None:
            return render(request, 'login.html',{"form":AuthenticationForm, "error":"Username or password incorrect"})
        
        login(request,user)
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user= request.user,finished__isnull = True)

    return render(request,'tasks.html',{"tasks":tasks}) 

@login_required
def tasks_finished(request):
    tasks = Task.objects.filter(user=request.user,finished__isnull = False).order_by('-finished')
    return render(request,'tasks_completed.html',{"tasks":tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,'create_task.html',{"form":TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit = False)
            new_task.user = request.user
            new_task.save()
            messages.success(request, "Task created succesfully")
            return redirect('tasks')
        except ValueError:
            
            return render(request, 'create_task.html',{"form":TaskForm,"error":"Error at creating task"})

@login_required
def completed_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'GET':
        task.finished = timezone.now()
        messages.success(request, "Task finished")
        task.save()
    return redirect('tasks_completed')

@login_required
def delete_task(request, task_id):
   
    if request.method == 'GET':
        task = get_object_or_404(Task,pk = task_id,user=request.user)
        messages.warning(request, "Task Deleted")
        task.delete()
    return redirect('tasks')
    
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
      
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            messages.success(request, "Task updated succesfully")
            form.save()
            return redirect('tasks')
        except ValueError:
            messages.error(request,"Error while updating task")
            return render(request, 'task_detail.html', {'task': task, 'form': form})
