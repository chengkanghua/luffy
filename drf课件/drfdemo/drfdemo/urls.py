"""drfdemo URL Configuration

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
from django.urls import path,include
from rest_framework.documentation import include_docs_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('stu/', include("students.urls")),
    path('ser/', include('sers.urls')),
    path('unser/',include('unsers.urls')),
    path('msers/',include('msers.urls')),
    path('req/',include('req.urls')),
    path('demo/',include('demo.urls')),
    path('gen/',include('gen.urls')),
    path('four/',include('four.urls')),
    path('docs/', include_docs_urls(title='站点页面标题')),

]
