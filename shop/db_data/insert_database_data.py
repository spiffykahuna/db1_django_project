#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def insert_categories():
    from db1_django_project.shop.models import Kauba_kategooria
    
    filename = os.path.join(os.path.dirname(__file__), 'goods_categories.txt')
    with open(filename) as category_file:
        for line in category_file:
            category = Kauba_kategooria()
            string = str(line.strip())
            category.name = string
            category.description = string
            try:
                category.save()
            except Exception as e:
                print 'Category is not saved to db: ', category.name
                print 'Details: ', e.message

if __name__ == '__main__':
    insert_categories()
    


                