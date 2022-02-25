from django.urls import path
from . import views

urlpatterns = [
    path('register_piece/', views.register_piece, name='register_piece'),
    path('get_board/', views.get_board, name='get_board'),
    path('get_board/<str:type>/', views.get_board, name='get_board'),
    path(
        'get_horse_movements/<str:origin>',
        views.get_horse_movements,
        name='get_horse_movements'
    ),
]
