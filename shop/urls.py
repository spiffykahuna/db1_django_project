#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Mar 26, 2012

@author: deko
'''
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import json_handler
from views import search_items
from views import show_user_favourites
from views import add_part_to_favourites
from views import delete_part_from_favourites
from views import show_user_parts
from views import show_user_profile

urlpatterns = patterns('',
                       url(r'^activate/complete/$',
                           direct_to_template,
                           {'template': 'registration/activation_complete.html'},
                           name='registration_activation_complete'),
                       url(r'^json/(?P<getParam>\w+)/$',
                           json_handler,
                           #{'backend': 'registration.backends.default.DefaultBackend'},
                           name='json_handler'),
                       url(r'^json/(?P<getParam>\w+)/(?P<paramValue1>\d+)$',
                           json_handler,
                           #{'backend': 'registration.backends.default.DefaultBackend'},
                           name='json_handler'),
                       url(r'^json/(?P<getParam>\w+)/(?P<paramValue1>\d+)/(?P<paramValue2>\d+)$',
                           json_handler,
                           #{'backend': 'registration.backends.default.DefaultBackend'},
                           name='json_handler'),
                       url(r'^$',
                           direct_to_template,
                           {'template': 'shop/shop_index.html'},
                           name='shop_index'),
                       url(r'^search/$',
                           search_items,
                           name='shop_search'),
                       
                       url(r'^favourites/$',
                           show_user_favourites,
                           name='show_user_favourites'),                       
                       url(r'^add_part_to_favourites/(?P<partId>\d+)$',
                           add_part_to_favourites,
                           name='add_part_to_favourites'),
                       url(r'^delete_part_from_favourites/(?P<partId>\d+)$',
                           delete_part_from_favourites,
                           name='delete_part_from_favourites'),
                       
                       url(r'^user_parts/$',
                           show_user_parts,
                           name='show_user_parts'),
                       
                       url(r'^user_profile/$',
                           show_user_profile,
                           name='show_user_parts'),
                       
                       
                       )