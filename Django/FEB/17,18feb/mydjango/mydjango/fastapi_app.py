from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from app.models import Project, ProjectCategory  
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

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

app = FastAPI()



# Request model for category
class CategoryCreate(BaseModel):
    name: str
    description: str

# Pydantic model for Project input
class ProjectCreate(BaseModel):
    name: str
    category_id: int
    # start_date: str
    # end_date: str = None
    # status: str = "Pending"

# Get all categories
@app.get("/")
def get_categories(request: Request):
    categories = ProjectCategory.objects.all()
    context = {
        "request": request,
        "title": "Categories Page",
        "categories": categories
    }
    return templates.TemplateResponse("index.html", context)

# to create category
@app.post("/create-category/")
async def create_category_post(name: str = Form(...), description: str = Form(...)):
    try:
        # Create instance without saving
        new_category = ProjectCategory(name=name, description=description)
        
        # Async save with validation
        await sync_to_async(new_category.save)(force_insert=True)
        
        return RedirectResponse(url="/", status_code=303)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Category already exists")

@app.get("/create-category/")
def create_category(request: Request):
    return templates.TemplateResponse("create-category.html", {"request": request})

# to update the details of a category 
@app.get("/update-category/{category_id}")
def edit_category(request: Request, category_id: int):
    try:
        category = ProjectCategory.objects.get(id=category_id)
        return templates.TemplateResponse("edit-category.html", {
            "request": request,
            "category": category,
            "title": "Update Category"})
    except ProjectCategory.DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found EDIT")
    

@app.post("/update-category/{category_id}")
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
@app.post("/delete-category/{category_id}")
def delete_category(category_id: int):
    try:
        category = ProjectCategory.objects.get(id=category_id)
        category.delete()
        return RedirectResponse(url="/", status_code=303)
    except ProjectCategory.DoesNotExist:
        raise HTTPException(status_code=404, detail="Category not found")


@app.get("/view-category/{category_id}")
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


# create new project inside category 
@app.get("/create-project/")
def create_project(request: Request, category_id: int = None):
    # You can use category_id to pre-populate or filter the form if needed.
    return templates.TemplateResponse("create-project.html", {"request": request, "category_id": category_id})

    











# Delete a category by ID
@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    category = ProjectCategory.objects.filter(id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.delete()
    return {"message": "Category deleted successfully"}

# Create Project
@app.post("/projects/")
def create_project(project_data: ProjectCreate):
    category = get_object_or_404(ProjectCategory, id=project_data.category_id)

    project = Project.objects.create(
        name=project_data.name,
        category=category,
        # start_date=project_data.start_date,
        # end_date=project_data.end_date,
        # status=project_data.status
    )
    return {"message": "Project created successfully", "project_id": project.id}

# Delete Project
@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return {"message": "Project deleted successfully"}