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
from fastapi import Query

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


# Delete a category by ID
@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    category = ProjectCategory.objects.filter(id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.delete()
    return {"message": "Category deleted successfully"}

##############################################################################################
# create new project inside category 
@app.get("/create-project/")
def create_project(request: Request, category_id: int = None):
    category = ProjectCategory.objects.get(id=category_id)
    
    return templates.TemplateResponse("create-project.html", {"request": request, "category_id": category_id, "category_name": category.name})

    
@app.post("/create-project/{category_id}")
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



@app.get("/edit-project/{category_id}/{project_id}")
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


@app.post("/edit-project/{category_id}/{project_id}")
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


@app.post("/delete-project/{category_id}/{project_id}")
def delete_project(category_id: int, project_id: int):
    try:

        project = Project.objects.get(id=project_id)
        project.delete()
        return RedirectResponse(url=f"/view-category/{category_id}", status_code=303)
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")






