from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register_piece/', views.register_piece, name='register_piece'),
]