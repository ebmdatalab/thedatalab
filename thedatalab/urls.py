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
from django.urls import path, re_path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .frontend import views
#from .frontend.models import Topic
from .frontend.models import Blog
from .frontend.models import Paper
from .frontend.models import Tool
from .frontend.models import Software
from .frontend.models import Dataset
from .frontend.models import Author


urlpatterns = [
    path('admin/', admin.site.urls),

    path('papers/<slug:slug>/', views.show_thing, {'thing_type': Paper}, name='show_paper'),
    path('blogs/<slug:slug>/', views.show_thing, {'thing_type': Blog}, name='show_blog'),
    path('tools/<slug:slug>/', views.show_thing, {'thing_type': Tool}, name='show_tool'),
    path('software/<slug:slug>/', views.show_thing, {'thing_type': Software}, name='show_software'),
    path('datasets/<slug:slug>/', views.show_thing, {'thing_type': Dataset}, name='show_dataset'),
    path('people/<slug:slug>/', views.show_thing, {'thing_type': Author}, name='show_author'),

    path('imagefit/', include('imagefit.urls')),
    path('markdownx/', include('markdownx.urls')),
    
    path('about-us/', views.team_index, name='team_index'),
    path('authors/<slug:slug>/', views.author_view, name='author_view'),
    path('blog/<int:year>/<int:month>/<int:pk>/<slug:slug>/', views.blog_post_redirect_view),
    path('blog/<int:pk>/<slug:slug>/', views.blog_post_view),
    path('papers/', views.paper_index, name='paper_index'),
    
    path('projects/<slug:slug>/', views.project_view, name='project_view'),
    path('topics/<slug:slug>/', views.topic_view, name='topic_index'),

    path(
        r"robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    
    path('search/', views.search_view, name='search'),

    path('', views.home_view, name='home'),
]


if settings.DEBUG is True:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

urlpatterns.extend([
    re_path(r'^(.*)$', views.page_view, name='page_view'),
])