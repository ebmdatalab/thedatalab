"""thedatalab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.conf.urls.static import static
from frontend import views
from frontend.models import Topic
from frontend.models import Blog
from frontend.models import Paper
from frontend.models import Tool
from frontend.models import Software
from frontend.models import Dataset


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/<slug:slug>/', views.show_thing, {'thing_type': Blog}, name='show_blog'),
    path('post/<slug:slug>/', views.show_thing, {'thing_type': Paper}, name='show_paper'),
    path('imagefit/', include('imagefit.urls')),
]


if settings.DEBUG is True:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
