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
from django.shortcuts import render,HttpResponse,redirect
from app_auth import models as auth_db
from app_log import models as log_db
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

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a)+int(b)
    return HttpResponse(str(c))

def goods(request):
    return render(request, 'news_goods.html')

class Goods(View):
    """商品管理"""


    def dispatch(self, request, *args, **kwargs):
        return super(Goods,self).dispatch(request, *args, **kwargs)

    def get(self,request):
        title = '商品管理'
        roles = auth_db.Role.objects.all()
        role_list = []
        for role in roles:
            role_list.append({"role_title": role.role_title, "role_id": role.id})

        #当前所有在线会话
        session_obj = Session.objects.all()
        online_user = []
        for i in session_obj:
            online_user.append(i.get_decoded()['user_name'])


        role_id = request.session['role_id']
        role_obj = auth_db.Role.objects.get(id=role_id)

        if role_obj.role_title == "administrator":
            user_info = auth_db.User.objects.all()
        else:
            user_name = request.session['user_name']
            user_info = auth_db.User.objects.filter(user_name=user_name)

        user_list = []
        for user in user_info:
            role_obj = user.role.all()
            role_title = []
            for i in  role_obj:
                    role_title.append(i.role_title)

            if user.user_name in online_user:
                status = "在线"
            else:
                status = "离线"

            user_list.append({"ready_name": user.ready_name, "user_id": user.id, "user_name": user.user_name,
                              'phone': user.phone, 'email': user.email, 'role_title': ",".join(role_title),
                              'status': status})

            user.status = status
            user.save()

        return render(request, 'rbac_user.html', locals())

