#!/usr/bin/python
# coding:utf-8
from django.contrib import admin
from .models import Article
from .models import Column
from .models import Userinfo


admin.site.register(Article)
admin.site.register(Column)
admin.site.register(Userinfo)
# Register your models here.
