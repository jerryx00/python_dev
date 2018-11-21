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

# 一本书由一家出版社出版，一家出版社可以出版很多书。一本书由多个作者合写，一个作者可以写很多书。
# 一个作者一个对应一个登录帐户
# 出版社
class Publisher(models.Model):
    name = models.CharField(max_length=20)
#作家表
class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    name = models.CharField(max_length=60, null=True)
    mobile = models.CharField(max_length=30, null=True)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return "%s %s %" % (self.name, self.first_name, self.last_name)

#出版物
class Book(models.Model):
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    pub = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)

    def __str__(self):              # __unicode__ on Python 2
        return self.title

    class Meta:
        ordering = ('title',)




@python_2_unicode_compatible
class Article(models.Model):
    column = models.ManyToManyField(Column, verbose_name='归属栏目')

    title = models.CharField('标题', max_length=256,null=False)
    slug = models.CharField('网址', max_length=256, db_index=True)

    author = models.ForeignKey(Author, blank=True, null=True, verbose_name='作者',on_delete=models.CASCADE)
    publications = models.ManyToManyField(Publisher)
    content = models.TextField('内容', default='', blank=True)

    published = models.BooleanField('正式发布', default=True)

    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '教程'
        verbose_name_plural = '教程'


#用户表
class Userinfo(models.Model):
    #如果没有models.AutoField，默认会创建一个id的自增列
    name = models.CharField(max_length=30)
    email = models.EmailField()
    memo = models.TextField()

#银行信息表
class Bankinfo(models.Model):
    #如果没有models.AutoField，默认会创建一个id的自增列
    name = models.CharField(max_length=30)
    email = models.EmailField()
    memo = models.TextField()

#电话信息表
class Phoneinfo(models.Model):
    #如果没有models.AutoField，默认会创建一个id的自增列
    name = models.CharField(max_length=30)
    email = models.EmailField()
    memo = models.TextField()


#教师表(教师id 教师姓名）
# 一个教师对应多个班级
class Teachers(models.Model):
    name = models.CharField(max_length=30)

# 学生表(学生id 学生姓名）
class Student(models.Model):
    name = models.CharField(max_length=30)

# 班级表(班级id 学生id)
# 一个班级对应多个学生
class Classes(models.Model):
    name = models.CharField(max_length=30)

# 课程表（课程id 课程名）
class Courses(models.Model):
    name = models.CharField(max_length=30)

# 成绩表 （学生id 课程id 分数）
class Score(models.Model):
    name = models.CharField(max_length=30)


#===========================================================
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):              # __unicode__ on Python 2
        return "%s the place" % self.name

class Restaurant(models.Model):
    # 在当前表中创建了一个字段 place_id 关联 Place 表
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):              # __unicode__ on Python 2
        return "%s the restaurant" % self.place.name

class Waiter(models.Model):
    #在当前表中创建了一个字段 restaurant_id 关联 Restaurant 表
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):              # __unicode__ on Python 2
        return "%s the waiter at %s" % (self.name, self.restaurant)


#==========================
class Province(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class City(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=5)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

#部门表
class Department(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):              # __unicode__ on Python 2
        return "the department code:%s,name: %s" % (self.code, self.name)

#枚举示例
#人员表
class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    # 在当前表中创建了一个字段 restaurant_id 关联 Restaurant 表,特性：外键、非空
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    visitation = models.ManyToManyField(City, related_name="visitor")
    hometown = models.ForeignKey(City, related_name="birth", on_delete=models.CASCADE, null=True)
    living = models.ForeignKey(City, related_name="citizen", on_delete=models.CASCADE, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return "name:%s " % (self.name)

#一对一
class Account(models.Model):
    name = models.CharField(max_length=60, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    created_at = models.DateField(auto_now=True, verbose_name='创建时间')
    updated_at = models.DateField(auto_now_add=True, verbose_name='修改时间')
    # 在当前表中创建了一个字段 userinfo_id 关联 Userinfo 表,特性：外键、非空、唯一
    userinfo = models.OneToOneField(Userinfo, on_delete=models.CASCADE)
    def __str__(self):              # __unicode__ on Python 2
        return "name:%s " % (self.name)








