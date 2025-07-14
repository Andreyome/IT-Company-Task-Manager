from django.contrib.auth.views import LogoutView
from django.urls import path

from task_catalog.views import (
    TaskCreateView,
    TaskDetailView,
    WorkerListView,
    WorkerDetailedView,
    TaskUpdateView,
    TaskDeleteView,
    WorkerDeleteView,
    CreatePosition,
    RegisterView,
    ProfileUpdateView,
    MarkTaskDoneView, CreateTaskTypeView, TaskBoardView,
)

app_name = "task_catalog"

urlpatterns = [
    path("", TaskBoardView.as_view(), name="index"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
    path("worker/", WorkerListView.as_view(), name="workers_list"),
    path("worker/<int:pk>/", WorkerDetailedView.as_view(), name="workers_detailed"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="workers_delete"),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-update'),
    path('tasks/<int:pk>/done/', MarkTaskDoneView.as_view(), name='task-done'),
    path('task-types/create/', CreateTaskTypeView.as_view(), name='tasktype-create'),
    path("positions/create/", CreatePosition.as_view(), name="position-create"),
]
