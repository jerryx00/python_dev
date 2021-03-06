"""minicms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from minicms import views
from django.urls import include
from app_auth.views import Index


urlpatterns = [
    path("",Index.as_view()),
    path('admin/', admin.site.urls),
    path("log/",include("app_log.urls")),
    path("auth/",include("app_auth.urls")),
    path("news/",include("news.urls")),

    path(r'leijun/', views.leijun),
]
