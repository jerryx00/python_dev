# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField('栏目名称', max_length=256)
    slug = models.CharField('栏目网址', max_length=256, db_index=True)
    intro = models.TextField('栏目简介', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '栏目'
        verbose_name_plural = '栏目'
        ordering = ['name']  # 按照哪个栏目排序


@python_2_unicode_compatible
class Article(models.Model):
    column = models.ManyToManyField(Column, verbose_name='归属栏目')

    title = models.CharField('标题', max_length=256)
    slug = models.CharField('网址', max_length=256, db_index=True)

    author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者',on_delete=models.CASCADE)
    content = models.TextField('内容', default='', blank=True)

    published = models.BooleanField('正式发布', default=True)

    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '教程'
        verbose_name_plural = '教程'

class Userinfo(models.Model):
    #如果没有models.AutoField，默认会创建一个id的自增列
    name = models.CharField(max_length=30)
    email = models.EmailField()
    memo = models.TextField()


class Test1(models.Model):
    #如果没有models.AutoField，默认会创建一个id的自增列
    name = models.CharField(max_length=30)
    email = models.EmailField()
    memo = models.TextField()

class Goods(models.Model):
    #如果没有models.AutoField，默认会创建一个id的自增列
    flxid = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    price = models.FloatField
    comment = models.CharField(max_length=30)




