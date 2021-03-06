"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from its_api.urls import router_projects, router_contributors, router_issues, router_comments
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('api/', include('users.urls')),
    path('api/projects/', include(router_projects.urls), name='api-root'),
    path('api/projects/<int:project_id>/', include(router_contributors.urls)),
    path('api/projects/<int:project_id>/', include(router_issues.urls)),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/', include(router_comments.urls))
]
