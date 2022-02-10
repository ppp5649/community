from django.urls import path
from . import views

urlpatterns = [
    path('job/', views.job, name='job'),
    path('major/', views.major, name='major'),
    path('<int:pk>/', views.board_detail, name='board_detail'),
    path('write/', views.board_write, name='board_write'),
]
