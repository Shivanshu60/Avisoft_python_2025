import os
import django

# Set the Django settings module and initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydjango.settings")
django.setup()

# Now import FastAPI and Django WSGI components
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application  # Use WSGI, not ASGI
from mydjango.fastapi_app import app as fastapi_app  # Import your FastAPI app

# Get Django's WSGI application
django_wsgi_app = get_wsgi_application()

# Mount Django (WSGI app) under '/django'
fastapi_app.mount("/django", WSGIMiddleware(django_wsgi_app))



# Expose the combined application as the ASGI callable
app = fastapi_app

from starlette.staticfiles import StaticFiles

# After setting up Django and FastAPI...
app.mount("/static", StaticFiles(directory="staticfiles"), name="static")