from django.db import models
from django.utils import timezone


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name="projects")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return self.name

class TaskAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="task_assignments")
    employee_name = models.CharField(max_length=255)
    task_description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_name} - {self.task_description} ({'Completed' if self.is_completed else 'Pending'})"