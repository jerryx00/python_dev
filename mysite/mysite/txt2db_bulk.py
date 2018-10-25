#!/usr/bin/env python
# coding:utf-8

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''

import django

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()


def main():
    from learn.models import Blog
    f = open('oldblog.txt')
    BlogList = []
    for line in f:
        parts = line.split('****')
        BlogList.append(Blog(title=parts[0], content=parts[1]))

    f.close()

    # 以上四行 也可以用 列表解析 写成下面这样
    # BlogList = [Blog(title=line.split('****')[0], content=line.split('****')[1]) for line in f]

    Blog.objects.bulk_create(BlogList)


if __name__ == "__main__":
    main()
    print('Done!')