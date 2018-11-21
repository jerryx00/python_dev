#!/usr/bin/python
# coding:utf-8
from django.shortcuts import render
from news.models import Userinfo, Person as PersonModel,Book as BookModel,Author,Publisher,Department,Restaurant,Waiter
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

        next_url = request.get_full_path()
        print(next_url)
        try:
            # django自带用户信息表
            author_obj = news_db.Author(name=name, email=email,mobile=mobile)
            author_obj.save()
            msg = "作者 %s 添加成功,请刷新查看！" % name
            data = {'msg':msg,'url':next_url}


        except Exception as e:
            msg = "作者添加失败：\n %s " % e
            data = {'msg': msg, 'url': next_url}

        data = json.dumps(data)
        return HttpResponse(data)

    def put(self,request):
        """修改用户"""
        req_info = eval(request.body.decode())
        author_id = req_info.get("author_id")
        name = req_info.get("name")
        mobile = req_info.get("mobile")
        email = req_info.get("email")
        action = req_info.get("action")

        next_url = request.get_full_path()

        if action:
            author_obj = news_db.Author.objects.get(id=author_id)
            author_obj.name = name
            author_obj.mobile = mobile
            author_obj.email = email
            author_obj.save()
            msg = "作者 %s 修改成功,请刷新查看！" % name
            data = {'msg': msg, 'url': next_url}
            data = json.dumps(data)

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


class Book(View):
    """书籍管理"""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Book,self).dispatch(request, *args, **kwargs)

    def get(self,request):
        title = '书籍管理'
        pubs = news_db.Publisher.objects.all()
        pub_list = []
        # print('get method,书籍管理查询界面')
        # for pub in pubs:
        #     pub_list.append({"pub_name": pub.name, "pub_id": pub.id})

        # 关联查询
        # blist = Book.objects.filter(id>0).values('publisher__name')
        book = BookModel.objects.select_related('pub__publisher').get(pk=1)
        # print(book)
        zhangs = PersonModel.objects.select_related('living__province').get(name=u"张")
        print(zhangs.living.province)


        return render(request, 'news_book.html', locals())

    def post(self, request):
        """添加书籍"""
        name = request.POST.get("name")
        title = request.POST.get("title")
        pub_id = request.POST.get("pub_id")

        next_url = request.get_full_path()

        try:
            # django自带用户信息表
            obj = news_db.Book(name=name,title=title, pub_id=pub_id)
            # print(pub_id)
            obj.save()

            msg = "书籍 %s 添加成功,请刷新查看！" % name
            data = {'code':0,'msg':msg,'url':next_url}


        except Exception as e:
            msg = "书籍添加失败：\n %s " % e
            data = {'code':1,'msg': msg, 'url': next_url}

        data = json.dumps(data)
        print(data)
        return HttpResponse(data)

    def put(self,request):
        """修改书籍"""
        req_info = eval(request.body.decode())
        book_id = req_info.get("book_id")
        name = req_info.get("name")
        title = req_info.get("title")

        action = req_info.get("action")

        next_url = request.get_full_path()

        if action:
            obj = news_db.Book.objects.get(id=book_id)
            obj.name = name
            obj.title = title
            obj.save()
            msg = "书籍 %s 修改成功,请刷新查看！" % name
            data = {'code':0,'msg': msg, 'url': next_url}
            data = json.dumps(data)

        else:
            """获取修改的书籍信息"""
            obj = news_db.Book.objects.get(id=book_id)
            data = json.dumps({'code':0,"name":obj.name, "title":obj.title,
                                        "author_id":obj.id})

        return HttpResponse(data)


    def delete(self,request):
        """删除书籍"""
        next_url = request.get_full_path()
        req_info = eval(request.body.decode())
        book_id = req_info.get("book_id")
        news_db.Book.objects.get(id=book_id).delete()
        msg = "书籍已删除,请刷新查看！"
        data = {'code': 0, 'msg': msg, 'url': next_url}
        data = json.dumps(data)
        return HttpResponse(data)


class Person(View):
    pass