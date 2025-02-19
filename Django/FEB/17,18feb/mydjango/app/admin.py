from django.contrib import admin
from .models import ProjectCategory, Project, TaskAssignment

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'category')
    search_fields = ('name',)

@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_name', 'project', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'project')
    search_fields = ('employee_name', 'task_description')
