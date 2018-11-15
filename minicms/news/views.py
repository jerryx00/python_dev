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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Author,self).dispatch(request, *args, **kwargs)

    def get(self,request):
        title = '作家管理'
        author_list = news_db.Author.objects.all()
        return render(request, 'news_author.html', locals())

    def post(self, request):
        """添加用户"""
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")

        try:
            # django自带用户信息表
            author_obj = news_db.Author(name=name, email=email,mobile=mobile)
            author_obj.save()
            data = "作者 %s 添加成功,请刷新查看！" % name

        except Exception as e:
            data = "作者添加失败：\n %s " % e

        return HttpResponse(data)

    def put(self,request):
        """修改用户"""
        req_info = eval(request.body.decode())
        author_id = req_info.get("author_id")
        name = req_info.get("name")
        mobile = req_info.get("mobile")
        email = req_info.get("email")
        action = req_info.get("action")
        if action:
            author_obj = news_db.Author.objects.get(id=author_id)
            author_obj.name = name
            author_obj.mobile = mobile
            author_obj.email = email
            author_obj.save()
            data = "作者 %s 修改成功,请刷新查看！" % name
        else:
            """获取修改的作者信息"""
            author_obj = news_db.Author.objects.get(id=author_id)
            data = json.dumps({"name":author_obj.name, "email":author_obj.email,
                                        "mobile":author_obj.mobile,"author_id":author_obj.id})

        return HttpResponse(data)


    def delete(self,request):
        """删除用户"""
        req_info = eval(request.body.decode())
        author_id = req_info.get("author_id")
        news_db.Author.objects.get(id=author_id).delete()
        data = "作者已删除,请刷新查看！"
        return HttpResponse(data)