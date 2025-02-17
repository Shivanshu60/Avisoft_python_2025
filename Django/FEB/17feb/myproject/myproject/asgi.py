"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi_app import app as fastapi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_asgi_application()
app = WSGIMiddleware(application)
app.mount("/api", fastapi_app)