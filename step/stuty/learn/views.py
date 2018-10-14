# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse(u"欢迎光临 自强学堂index!")
