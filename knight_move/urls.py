from django.urls import path
from . import views

urlpatterns = [
    path('register_piece/', views.register_piece, name='register_piece'),
    path('get_board/', views.get_board, name='get_board'),
    path('get_board/<str:type>/', views.get_board, name='get_board'),
    path(
        'get_knight_movements/<str:origin>',
        views.get_knight_movements,
        name='get_knight_movements'
    ),
]
