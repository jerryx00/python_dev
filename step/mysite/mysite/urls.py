# coding:utf-8

from django.contrib import admin
from django.urls import path
from learn import views as learn_views  # new

urlpatterns = [
    path('', learn_views.index),  # new
    path('add/', learn_views.add, name='add'),  # new
    path('add/<int:a>/<int:b>/', learn_views.add2, name='add2'),  # new
    path('view/', learn_views.view, name='view'),  # new
    path('admin/', admin.site.urls),
]
