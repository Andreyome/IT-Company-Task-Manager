from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Case, When, Value, IntegerField, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, FormView, TemplateView

from task_catalog.forms import TaskForm, SignUpForm, WorkerUpdateForm, PositionForm
from task_catalog.models import Worker, Task, TaskType, Position


class TaskBoardView(TemplateView):
    template_name = 'task_catalog/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')

        priority_order = Case(
            When(priority="Urgent", then=Value(0)),
            When(priority="High", then=Value(1)),
            When(priority="Medium", then=Value(2)),
            When(priority="Low", then=Value(3)),
            output_field=IntegerField()
        )

        base_queryset = Task.objects.annotate(priority_rank=priority_order)

        if query:
            base_queryset = base_queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        todo_tasks = base_queryset.filter(is_completed=False).order_by('priority_rank', 'deadline')
        done_tasks = base_queryset.filter(is_completed=True).order_by('priority_rank', 'deadline')

        todo_paginator = Paginator(todo_tasks, 3)
        done_paginator = Paginator(done_tasks, 3)

        context.update({
            'q': query,
            'todo_page': todo_paginator.get_page(self.request.GET.get('todo_page')),
            'done_page': done_paginator.get_page(self.request.GET.get('done_page')),
        })
        return context


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


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('task_catalog:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = WorkerUpdateForm
    template_name = 'task_catalog/profile_update.html'
    success_url = reverse_lazy('task_catalog:workers_list')

    def get_object(self):
        return self.request.user


class MarkTaskDoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = True
        task.save()
        return redirect('task_catalog:index')


class CreateTaskTypeView(LoginRequiredMixin, View):
    def post(self, request):
        name = request.POST.get("name")
        if name:
            TaskType.objects.get_or_create(name=name)
        return redirect(request.META.get('HTTP_REFERER', 'task_catalog:task-list'))


class CreatePosition(LoginRequiredMixin, CreateView):
    model = Position
    form_class = PositionForm

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse_lazy('task_catalog:worker-list'))
