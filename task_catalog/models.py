from django.contrib.auth.models import AbstractUser
from django.db import models


class Worker(AbstractUser):
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name}) Position: {self.position}"


class TaskType(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    workers = models.ManyToManyField(Worker, related_name="tasks")
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}: {self.priority}. {self.description} ({self.deadline}) is: {self.is_completed} workers: {self.assignees.count()}"





class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name