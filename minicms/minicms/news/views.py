#!/usr/bin/python
# coding:utf-8
from django.shortcuts import render

# Create your views here
def show(request):
    from .models import Userinfo
    list = models.UserInfo.objects.all()
    print 'aa'
    pass
