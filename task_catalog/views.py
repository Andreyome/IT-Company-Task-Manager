from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from task_catalog.forms import TaskForm, SignUpForm, WorkerUpdateForm
from task_catalog.models import Worker, Task, TaskType, Position


def task_board_view(request):
    query = request.GET.get('q', '')

    base_queryset = Task.objects.all()

    if query:
        base_queryset = base_queryset.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    todo_tasks = base_queryset.filter(is_completed=False)
    done_tasks = base_queryset.filter(is_completed=True)

    todo_paginator = Paginator(todo_tasks, 5)
    done_paginator = Paginator(done_tasks, 5)

    todo_page_number = request.GET.get('todo_page')
    done_page_number = request.GET.get('done_page')

    context = {
        'q': query,
        'todo_page': todo_paginator.get_page(todo_page_number),
        'done_page': done_paginator.get_page(done_page_number),
    }
    return render(request, 'task_catalog/task_list.html', context)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = "/"


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_catalog:index")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task_catalog:index")

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker


class WorkerDetailedView(LoginRequiredMixin, DetailView):
    model = get_user_model()


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Worker
    success_url = reverse_lazy("task_catalog:workers_list")


def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_catalog:index')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = WorkerUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_catalog:workers_list')
    else:
        form = WorkerUpdateForm(instance=request.user)
    return render(request, 'task_catalog/profile_update.html', {'form': form})

@login_required
def mark_task_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.is_completed = True
        task.save()
    return redirect('task_catalog:index')

@login_required
def create_task_type(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            TaskType.objects.get_or_create(name=name)
    return redirect(request.META.get('HTTP_REFERER', 'task_catalog:task-list'))

@login_required
def create_position(request):
    name = request.POST.get("name")
    if name:
        Position.objects.get_or_create(name=name)
    return redirect(request.META.get('HTTP_REFERER', 'task_catalog:worker-list'))
