#!/usr/bin/python
# coding:utf-8
from django.shortcuts import render
from news.models import Userinfo
from pprint import pprint
from django.http import HttpResponse

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
