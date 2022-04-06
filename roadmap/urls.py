"""roadmap URL Configuration

The `urlpatterns` list routes URLs to views. For more inion please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from board.views import comment_write, comment_delete
from main.views import index
from user.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('board/', include('board.urls')),
    path('user/', include('user.urls')),
    path('', home, name='home'),
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('comment_write/<int:pk>', comment_write, name="comment_write"),
    path('comment_delete/<int:pk>/<int:com_id>',
         comment_delete, name="comment_delete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
