from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('job/', views.job, name='job'),
    path('major/', views.major, name='major'),
    path('<int:pk>/', views.board_detail, name='board_detail'),
    path('write/', views.board_write, name='board_write'),
    path('<int:pk>/update/', views.board_update, name='board_update'),
    path('<int:pk>/delete/', views.board_delete, name='board_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
