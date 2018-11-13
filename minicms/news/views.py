#!/usr/bin/python
# coding:utf-8
from django.shortcuts import render
from news.models import Userinfo
from pprint import pprint
from django.http import HttpResponse
import datetime
import json,re
# import redis
# from statics.scripts import encryption
# from mtrops_v2.settings import SECRET_KEY,DATABASES,REDIS_INFO
from django.views import View
from news import views
from django.shortcuts import render,HttpResponse,redirect
from news import models as news_db
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from app_auth.perms_control import menus_list,perms_list
from django.contrib.sessions.models import Session

def index(request):
    # return HttpResponse(u"welcome!")
    return render(request, 'home.html')

# Create your views here
def user_index(request):
    user_list = Userinfo.objects.all()
    # return HttpResponse(u"欢迎光临!")
    return render(request, 'user_index.html',{'user_list':user_list})

def prn_obj(obj):
    pprint(vars(obj))

def view(request):
    return render(request, 'view.html')

def goods(request):
    return render(request, 'news_goods.html')

class Author(View):
    """作家管理"""
    def dispatch(self, request, *args, **kwargs):
        return super(Author,self).dispatch(request, *args, **kwargs)

    def get(self,request):
        title = '作家管理'
        author_list = news_db.Author.objects.all()
        return render(request, 'news_author.html', locals())