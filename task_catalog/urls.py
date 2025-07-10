from django.contrib.auth.views import LogoutView
from django.urls import path

from task_catalog.views import (
    TaskCreateView,
    TaskDetailView,
    WorkerListView,
    WorkerDetailedView,
    task_board_view,
    TaskUpdateView,
    TaskDeleteView,
    WorkerDeleteView,
    register_view, update_profile, mark_task_done, create_task_type, create_position
)

app_name = "task_catalog"

urlpatterns = [
    path("", task_board_view, name="index"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
    path("worker/", WorkerListView.as_view(), name="workers_list"),
    path("worker/<int:pk>/", WorkerDetailedView.as_view(), name="workers_detailed"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="workers_delete"),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/edit/', update_profile, name='profile-update'),
    path('tasks/<int:pk>/done/', mark_task_done, name='task-done'),
    path('task-types/create/', create_task_type, name='tasktype-create'),
    path("positions/create/", create_position, name="position-create"),
]
