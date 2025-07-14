from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from task_catalog.models import Task, Position, TaskType, Worker


class ModelsTest(TestCase):
    def test_task_str(self):
        task = Task.objects.create(
            name="Task 1",
            description="Task description",
            deadline=datetime.now(),
            is_completed=False,
            priority=1,
        )
        self.assertEqual(str(task), f"{task.name}: {task.priority}. {task.description} ({task.deadline}) is: {task.is_completed} workers: {task.workers.count()}")

    def test_position_str(self):
        position = Position.objects.create(
            name="Position 1",
        )
        self.assertEqual(str(position), f"{position.name}")

    def test_position_task_type_str(self):
        task_type = TaskType.objects.create(
            name="Task Type 1",
        )
        self.assertEqual(str(task_type), f"{task_type.name}")

    def test_worker_str(self):
        position = Position.objects.create(
            name="Position 1",
        )
        worker = get_user_model().objects.create(
            username="Worker 1",
            position=position,
        )
        self.assertEqual(str(worker), f"{worker.username} Position: {worker.position}")