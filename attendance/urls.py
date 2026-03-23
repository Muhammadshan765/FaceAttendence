from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('recognize/', views.recognize, name='recognize'),
    path('history/', views.history, name='history'),
    
    # APIs
    path('api/register_face/', views.register_face, name='register_face'),
    path('api/recognize_face/', views.recognize_face, name='recognize_face'),
    path('api/export_csv/', views.export_csv, name='export_csv'),
]
