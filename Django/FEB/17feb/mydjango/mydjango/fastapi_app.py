from fastapi import FastAPI
from pydantic import BaseModel
from asgiref.sync import sync_to_async

# Import Django models from the app package
from app.models import Category, Project, Employee

# Initialize FastAPI
app = FastAPI(title="Combined FastAPI and Django App")

# Pydantic models for serialization/validation
class EmployeeOut(BaseModel):
    name: str
    task: str

class ProjectOut(BaseModel):
    name: str
    employees: list[EmployeeOut]

class CategoryOut(BaseModel):
    name: str
    projects: list[ProjectOut]

# Async wrapper for Django ORM queries
async def get_all(queryset):
    return await sync_to_async(list)(queryset)

# Endpoint to fetch all categories with projects and employees
@app.get("/categories", response_model=list[CategoryOut])
async def get_categories():
    categories = await get_all(Category.objects.all())
    category_list = []
    for category in categories:
        projects = await get_all(Project.objects.filter(category=category))
        project_list = []
        for project in projects:
            employees = await get_all(Employee.objects.filter(project=project))
            employee_list = [EmployeeOut(name=emp.name, task=emp.task) for emp in employees]
            project_list.append(ProjectOut(name=project.name, employees=employee_list))
        category_list.append(CategoryOut(name=category.name, projects=project_list))
    return category_list
