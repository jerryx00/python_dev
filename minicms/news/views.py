#!/usr/bin/python
# coding:utf-8
from django.shortcuts import render
from news.models import Userinfo
from pprint import pprint
from django.http import HttpResponse

# Create your views here
def show(request):
    list = Userinfo.objects.all()
    return HttpResponse(u"欢迎光临!")

def prn_obj(obj):
    pprint(vars(obj))
