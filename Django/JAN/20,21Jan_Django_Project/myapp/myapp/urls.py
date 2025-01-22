"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),  # Home page
    path('home/view-para/<int:id>/', views.view_para, name='view_para'),  # View paragraph by ID
    path('home/download-para/<int:id>/', views.download_para, name='download_para'),  # Download paragraph
    path('home/delete-para/<int:id>/', views.delete_para, name='delete_para'),  # Delete paragraph
    path('home/save-para/', views.save_para, name='save_para'),  # Save paragraph
    path('downloads/', views.downloads, name='downloads'),  # Downloads page
    path('about/', views.about, name='about'),  # About page
    path('auth/', include('auth_app.urls')),  # Authentication app URLs
]

# Let Django handle 404 and serve the static content
handler404 = 'myapp.views.custom_404'




