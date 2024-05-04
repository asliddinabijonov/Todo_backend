from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.contrib.auth import authenticate, login, logout


class TaskListView(View):
    def get(self, request):
        if request.user.is_authenticated:
            tasks = Task.objects.filter(user=request.user)
            context = {
                'tasks': tasks,
                'user': request.user,
                'status_choise': Task.STATUS_CHOICES,
            }
            return render(request, 'index.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            title = request.POST.get('name', None)
            description = request.POST.get('details', None)
            deadline = request.POST.get('date', None)
            status = request.POST.get('status', None)
            if title:
                new_task = Task.objects.create(
                    title=title,
                    description=description,
                    deadline=deadline,
                    status=status,
                    user=request.user
                )
                new_task.save()
                if new_task.deadline == "2000-01-01":
                    new_task.deadline = None
                    new_task.save()
                return redirect('index')


class EditTaskView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            task = Task.objects.get(id=pk)
            if request.user != task.user:
                return redirect('index')
            context = {
                'task': task,
                'status_choise': Task.STATUS_CHOICES,
            }
            return render(request, 'edit.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            task = Task.objects.get(id=pk)
            if request.user == task.user:
                task.title = request.POST.get('title', None),
                task.description = request.POST.get('description', None),
                task.status = request.POST.get('status', None),
                task.save()
            return redirect('index')
        return redirect('login')


class LoginTaskView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('index')
        return redirect('login')


class LogoutTaskView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class DeleteTaskView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            task = get_object_or_404(Task, pk=pk)
            if task.user == request.user:
                task.delete()
                return redirect('index')
            return redirect('logout')
        return redirect('login')


class RegisterTaskView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        try:
            User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        except(ValueError):
            return redirect('login')
        return redirect('login')
