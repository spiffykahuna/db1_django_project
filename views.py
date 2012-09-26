#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Sep 25, 2011

@author: deko
'''
from django.http import HttpResponse 
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from django import forms
from django.contrib.auth.forms import UserCreationForm


import datetime


def hello(request):
    return HttpResponse("Hello world")

def my_homepage_view(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render_to_response('hours_ahead.html', {'hour_offset': offset,
                                                   'next_time': dt})
    

def debug(request):
    return HttpResponseRedirect('/')



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/books/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    })
