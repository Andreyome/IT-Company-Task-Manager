from django.contrib.auth.models import AbstractUser
from django.db import models



class Task(models.Model):
    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}: {self.priority}. {self.description} ({self.deadline}) is: {self.is_completed} workers: {self.assignees.count()}"


class Worker(AbstractUser):
    tasks = models.ManyToManyField(Task, related_name="assignees")

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

class TaskType(models.Model):
    name = models.CharField(max_length=255)
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_types")
    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)
    workers = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="position")

    def __str__(self):
        return self.name