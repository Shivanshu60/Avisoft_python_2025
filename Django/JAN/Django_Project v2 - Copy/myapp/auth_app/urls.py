from django.urls import path
from . import views  # Import views from auth_app (register, login, logout)
from myapp import views as myapp_views  # Import views from myapp (only for home view)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # path('home/', myapp_views.home, name='home'),  # Reference home view from myapp
]
