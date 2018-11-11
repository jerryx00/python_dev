#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-07-28 20:38:38
# @Author  : Weizhong Tu (mail@tuweizhong.com)
# @Link    : http://www.tuweizhong.com

'''
create some records for demo database
'''

from minicms.wsgi import *
from news.models import Place,Restaurant,Waiter


def main():
    p1 = Place(name='Demon Dogs', address='944 W. Fullerton')
    p1.save()
    p2 = Place(name='Ace Hardware', address='1013 N. Ashland')
    p2.save()

    r = Restaurant(place=p1, serves_hot_dogs=True, serves_pizza=False)
    r.save()

if __name__ == '__main__':
    main()
    print("Done!")