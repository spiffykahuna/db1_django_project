#!/usr/bin/env python
# -*- coding: utf-8 -*

from db1_django_project.registration.backends.default import DefaultBackend
from django.contrib.sites.models import Site, RequestSite
from db1_django_project.registration.models import RegistrationProfile
from db1_django_project.registration import signals
from db1_django_project.registration.forms import RegistrationFormCustom,\
    RegistrationForm
from db1_django_project.shop.models import Auto_mudel, Mootor, Auto_mark, Klient,\
    Auto_modifikatsioon
from django.contrib.auth.models import User




    


class CustomShopBackend(DefaultBackend):
    """
        This is custom backend that adds some new fields to registration form.
        It creates new UserProfile with information about users car 
    """
    @staticmethod
    def get_car_details(make_id, model_id, engine_id):
        try:
            # if not present
            if not (make_id and model_id and engine_id):
                make = None
                model = None
                raise Mootor.DoesNotExist('whatever')
            
            make = Auto_mark.objects.get(auto_mark_id=make_id)
            model = Auto_mudel.objects.get(auto_mudel_id=model_id)
            engine = Mootor.objects.get(mootor_id=engine_id)  
            
        except Auto_mark.DoesNotExist:
            make = None              
            model = None
            engine = None
        except Auto_mudel.DoesNotExist:
            model = None
            engine = None
        except Mootor.DoesNotExist:
            engine = None
            
        return (make, model, engine)
    
    @staticmethod
    def save_user_car(make, model, engine, new_user):
        if not (make and model and engine):
            return False
        try:
            klient = Klient.objects.get(user=new_user)
            auto = Auto_modifikatsioon.objects.get(auto_mudel=model,
                                                   mootor=engine)
            klient.kliendi_auto = auto
            klient.save()          
          
            
        except Klient.DoesNotExist:            
            
            
            new_user.save()
            
            auto = Auto_modifikatsioon.objects.get(auto_mudel=model,
                                                   mootor=engine)
             
            klient = Klient(user=new_user, kliendi_auto=auto)
            
            klient.username = new_user.username
            klient.first_name = new_user.first_name
            klient.last_name = new_user.last_name
            klient.email = new_user.email
            klient.password = new_user.password
            klient.is_staff = new_user.is_staff
            klient.is_active = new_user.is_active
            klient.is_superuser = new_user.is_superuser
            klient.last_login = new_user.last_login
            klient.date_joined = new_user.date_joined
            
            klient.save()
            
        except Auto_modifikatsioon.DoesNotExist:
            raise        
        return True

    def register(self, request, **kwargs):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The emakeyword argument.il will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        make, model_id, engine_id = (kwargs['make'],
                                     int(kwargs['model']),
                                     int(kwargs['engine']))
        if make and make.auto_mark_id:
            make, model, engine = self.get_car_details(make.auto_mark_id, model_id, engine_id)
        else:
            make, model, engine = self.get_car_details(None, model_id, engine_id)
        
            
       
        
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                    password, site)
        
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        
        self.save_user_car(make, model, engine, new_user)
        
        return new_user


    def get_form_class(self, request):
            """
            Return the custom form with some additional fields
            
            """
            return RegistrationFormCustom
            #return RegistrationForm
            
    def post_registration_redirect(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.
        
        """
        url = '/accounts/register/complete/' + user.email
        #return ('registration_complete_with_email', email , {})
        return (url, (), {})                