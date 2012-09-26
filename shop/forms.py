#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Apr 26, 2012

@author: deko
'''

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from db1_django_project.registration.forms import RegistrationFormCustom

attrs_dict = {'class': 'required'}


def order_fields(*field_list):
    def decorator(form):
        original_init = form.__init__
        def init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)        
            for field in field_list[::-1]:
                self.fields.insert(0, field, self.fields.pop(field))
        form.__init__ = init
        return form            
    return decorator

@order_fields('username',
              'first_name',
              'last_name',
              'email',
              'old_password')
class UserProfileForm(RegistrationFormCustom):
    first_name = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("First name*"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    last_name = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Last name*"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    
    old_password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                   required=False,
                                label=_("Old password"))
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)        
        self.fields['password1'].label = _("New Password")
        self.fields['password1'].required = False
                
        self.fields['password2'].label = _("New Password (again)")        
        self.fields['password2'].required = False
        
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        return self.cleaned_data['username']
        
#        try:
#            username = super(UserProfileForm, self).clean_username()
#                        
#            user = User.objects.get(username__iexact=username)
#        except User.DoesNotExist:
#            return self.cleaned_data['username']
#        except forms.ValidationError:
#            pass
#        raise forms.ValidationError(_("A user with that username already exists."))
    
    def check_username_presense(self, userName):
        try:
            user = User.objects.get(username__iexact=userName)
            return True
        except User.DoesNotExist:
            return False
        return True