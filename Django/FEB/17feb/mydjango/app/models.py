from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='employees', on_delete=models.CASCADE)
    task = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.task}"
