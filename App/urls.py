from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_image, name='generate_image'),
    path('results/<int:pk>/', views.check_generation, name='check_generation'),
]