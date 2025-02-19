from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from app.models import Project, ProjectCategory, TaskAssignment 
from django.db.utils import IntegrityError
from fastapi import FastAPI
from django.shortcuts import get_object_or_404
from fastapi.templating import Jinja2Templates
from django.conf import settings
from fastapi import Form
from fastapi.responses import RedirectResponse
from asgiref.sync import sync_to_async
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from fastapi import Query

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

app = FastAPI()

#########################################################################################
#Schemas

#for category
class CategoryCreate(BaseModel):
    name: str
    description: str

#  for Project input
class ProjectCreate(BaseModel):
    name: str
    category_id: int
    # start_date: str
    # end_date: str = None
    # status: str = "Pending"

##########################################################################################
# APIS
#for category


# Get all categories
@app.get("/",  tags=["Category"])
def get_categories(request: Request):
    categories = ProjectCategory.objects.all()
    context = {
        "request": request,
        "title": "Categories Page",
        "categories": categories
    }
    return templates.TemplateResponse("index.html", context)

# to create category
@app.post("/create-category/", tags=["Category"])
async def create_category_post(name: str = Form(...), description: str = Form(...)):
    try:
        # Create instance new
        new_category = ProjectCategory(name=name, description=description)
        
        # Async save with validation
        await sync_to_async(new_category.save)(force_insert=True)
        
        return RedirectResponse(url="/", status_code=303)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Category already exists")

@app.get("/create-category/", tags=["Category"])
def create_category(request: Request):
    return templates.TemplateResponse("create-category.html", {"request": request})

# to update the details of a category 
@app.get("/update-category/{category_id}", tags=["Category"])
def edit_category(request: Request, category_id: int):
    try:
        category = ProjectCategory.objects.get(id=category_id)
        return templates.TemplateResponse("edit-category.html", {
            "request": request,
            "category": category,
            "title": "Update Category"})
    except ProjectCategory.DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found EDIT")
    

@app.post("/update-category/{category_id}", tags=["Category"])
def update_category(category_id: int, name: str = Form(...), description: str = Form(...)):
    print(f"Received form data - name: {name}, description: {description}")
    try:
        category = ProjectCategory.objects.get(id=category_id)
        category.name = name
        category.description = description
        category.save()
        return RedirectResponse(url="/", status_code=303)
    except ProjectCategory.DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")



# to delete a category 
@app.post("/delete-category/{category_id}", tags=["Category"])
def delete_category(category_id: int):
    try:
        category = ProjectCategory.objects.get(id=category_id)
        category.delete()
        return RedirectResponse(url="/", status_code=303)
    except ProjectCategory.DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")


@app.get("/view-category/{category_id}", tags=["Category"])
def view_category(request: Request, category_id: int):
    try:
        # Get the category using the Django ORM
        category = ProjectCategory.objects.get(id=category_id)
    except ProjectCategory.DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Retrieve all projects associated with this category using the related name
    projects = category.projects.all()
    
    # Prepare context for the template
    context = {
        "request": request,
        "category": category,
        "projects": projects,
    }
    return templates.TemplateResponse("view-category.html", context)


# Delete a category by ID
@app.post("/categories/{category_id}", tags=["Category"])
def delete_category(category_id: int):
    category = ProjectCategory.objects.filter(id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.delete()
    return {"message": "Category deleted successfully"}

##############################################################################################
# PROJECT related apis

@app.get("/create-project/", tags=["Project"])
def create_project(request: Request, category_id: int = None):
    category = ProjectCategory.objects.get(id=category_id)
    
    return templates.TemplateResponse("create-project.html", {"request": request, "category_id": category_id, "category_name": category.name})

    
@app.post("/create-project/{category_id}", tags=["Project"])
def save_project(
    category_id: int,
    name: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    status: str = Form(...),
):
    try:
        category = ProjectCategory.objects.get(id=category_id)
        new_project = Project.objects.create(
            category=category,
            name=name,
            start_date=start_date,
            end_date=end_date,
            status=status,
        )
        return RedirectResponse(url=f"/view-category/{category_id}", status_code=303)
    except ObjectDoesNotExist:
        return {"error": "Category not found"}



@app.get("/edit-project/{category_id}/{project_id}", tags=["Project"])
def edit_project(request: Request, category_id: int, project_id: int):
    try:
        project = Project.objects.get(id=project_id)
        return templates.TemplateResponse(
            "edit-project.html",
            {
                "request": request,
                "project": project,
                "category_id": category_id  # Pass category_id to the template if needed
            }
        )
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")


@app.post("/edit-project/{category_id}/{project_id}", tags=["Project"])
def update_project(
    category_id: int,
    project_id: int,
    name: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    status: str = Form(...),
):
    try:
        project = Project.objects.get(id=project_id)
        # Update the project with the new data
        project.name = name
        project.start_date = start_date
        project.end_date = end_date
        project.status = status
        project.save()
        # Redirect back to the category page using the category_id from the URL
        return RedirectResponse(url=f"/view-category/{category_id}", status_code=303)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")


@app.post("/delete-project/{category_id}/{project_id}", tags=["Project"])
def delete_project(category_id: int, project_id: int):
    try:

        project = Project.objects.get(id=project_id)
        project.delete()
        return RedirectResponse(url=f"/view-category/{category_id}", status_code=303)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")



@app.get("/view-project/{category_id}/{project_id}", tags=["Project"])
def view_project(request: Request, category_id: int, project_id: int):
    try:
        # Ensure that the project belongs to the specified category
        project = Project.objects.get(id=project_id, category__id=category_id)
        category = project.category  # Extract the category from the project
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get all task assignments for this project (assuming the related_name is "task_assignments")
    tasks = project.task_assignments.all()
    
    # Render the template with the project, its tasks, and its category
    return templates.TemplateResponse("view-project.html", {
        "request": request,
        "project": project,
        "tasks": tasks,
        "category": category
    })


#####################################################################
# EMPLOYEE/TASK PART

@app.get("/add-task/{category_id}/{project_id}", tags=["Employee Task"])
def add_task_form(request: Request, category_id: int, project_id: int):
    try:
        project = Project.objects.get(id=project_id, category__id=category_id)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Render a template that shows a form for adding a new task assignment
    return templates.TemplateResponse("add-task.html", {
        "request": request,
        "project": project,
        "category": project.category
    })


@app.post("/add-task/{category_id}/{project_id}", tags=["Employee Task"])
def create_task(
    category_id: int,
    project_id: int,
    employee_name: str = Form(...),
    task_description: str = Form(...),
    is_completed: bool = Form(False)  # Checkbox returns False if not checked
):
    try:
        project = Project.objects.get(id=project_id, category__id=category_id)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create the task assignment
    TaskAssignment.objects.create(
        project=project,
        employee_name=employee_name,
        task_description=task_description,
        is_completed=is_completed
    )
    
    # Redirect back to the project view page
    return RedirectResponse(url=f"/view-project/{category_id}/{project_id}", status_code=303)


@app.get("/edit-task/{category_id}/{project_id}/{task_id}", tags=["Employee Task"])
def edit_task_form(request: Request, category_id: int, project_id: int, task_id: int):
    try:
        # Ensure the project exists and belongs to the given category
        project = Project.objects.get(id=project_id, category__id=category_id)
        # Ensure the task belongs to this project
        task = TaskAssignment.objects.get(id=task_id, project=project)
    except (Project.DoesNotExist, TaskAssignment.DoesNotExist):
        raise HTTPException(status_code=404, detail="Project or Task not found")
    
    # Render the template with the current task data
    return templates.TemplateResponse("edit-task.html", {
        "request": request,
        "project": project,
        "category": project.category,
        "task": task
    })

@app.post("/edit-task/{category_id}/{project_id}/{task_id}", tags=["Employee Task"])
def update_task(
    category_id: int,
    project_id: int,
    task_id: int,
    employee_name: str = Form(...),
    task_description: str = Form(...),
    is_completed: bool = Form(False)  # Checkbox returns False if not checked
):
    try:
        project = Project.objects.get(id=project_id, category__id=category_id)
        task = TaskAssignment.objects.get(id=task_id, project=project)
    except (Project.DoesNotExist, TaskAssignment.DoesNotExist):
        raise HTTPException(status_code=404, detail="Project or Task not found")
    
    # Update the task assignment
    task.employee_name = employee_name
    task.task_description = task_description
    task.is_completed = is_completed
    task.save()
    
    # Redirect back to the project view page
    return RedirectResponse(url=f"/view-project/{category_id}/{project_id}", status_code=303)


@app.post("/delete-task/{category_id}/{project_id}/{task_id}", tags=["Employee Task"])
def delete_task(category_id: int, project_id: int, task_id: int):
    try:
        project = Project.objects.get(id=project_id, category__id=category_id)
        task = TaskAssignment.objects.get(id=task_id, project=project)
    except (Project.DoesNotExist, TaskAssignment.DoesNotExist):
        raise HTTPException(status_code=404, detail="Project or Task not found")
    
    # Delete the task assignment
    task.delete()
    
    # Redirect back to the project view page
    return RedirectResponse(url=f"/view-project/{category_id}/{project_id}", status_code=303)
