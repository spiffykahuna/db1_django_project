#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse 
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import render_to_response

from django.core import serializers

from models import Auto_mark
from models import Auto_mudel
from models import Varuosa_kategooria
from models import Auto_modifikatsioon
from models import Varuosa
from models import Lemmik_varuosa
from models import Klient

from django.contrib.auth.decorators import login_required
#from db1_django_project.shop.models import Kliendi_auto
from db1_django_project.shop.forms import UserProfileForm
from db1_django_project.registration.backends.custom import CustomShopBackend
from database_storage.database_storage import DatabaseStorage
from db1_django_project import settings
import mimetypes
from django.contrib.auth.models import User



def request_type_required(f, request_type='POST'):
    """
        Decorator checks for request type
        if type is wrong it returns wrong message
    """
    def check_request(request, *args, **kwargs):
        if request_type == request.META['REQUEST_METHOD']:
            res = f(request, *args, **kwargs)
            return res
        else:
            responseText = ('\nWrong request type: ' 
                                       + request.META['REQUEST_METHOD'] +
                                       '\nneed to be {0}').format(request_type)
            return HttpResponseServerError(responseText)  

    return check_request


def get_goods_categories(request):
    data = serializers.serialize("json", Varuosa_kategooria.objects.all())
    return HttpResponse(data)
    
def get_car_mark(request):    
    data = serializers.serialize("json", Auto_mark.objects.all())
    return HttpResponse(data)

def get_car_model_by_mark_id(mark_id):
    try:
        mark_id = int(mark_id)
        data = serializers.serialize("json",
                                      Auto_mudel.objects.filter(auto_mark=mark_id))
        return HttpResponse(data)
    except:
        pass
    

def get_engines_by_make_and_model(paramValue1, paramValue2):
    if not (paramValue1 and paramValue2):        
        return HttpResponse('Specify make and model')
    make_id = int(paramValue1)
    model_id = int(paramValue2)
    # get engines Ids
    omamised = Auto_modifikatsioon.objects.filter(auto_mudel=model_id)
    engines = []
    for omamine in omamised:
        engines.append(omamine.mootor) 
               
    data = serializers.serialize("json", engines)
    return HttpResponse(data)    
                                            
    
    

@login_required(login_url='/accounts/login/')
def get_user_car_details(request):
    """
        returns user's car details ( make, model, engine) 
    """
    import json
    try:    
        klient = Klient.objects.get(user=request.user)
        car = klient.kliendi_auto        
    except Klient.DoesNotExist:
        car = None
    if not car:
        return HttpResponseServerError('hothing found. there is no car specified for this user')
    
    carDetails = {'fields': {
                             'mootor': car.mootor.mootor_id,
                             'auto_mudel': car.auto_mudel.auto_mudel_id,
                             'auto_mark': car.auto_mudel.auto_mark.auto_mark_id                             
                             },
                  
                  }
    car.auto_mark = car.auto_mudel.auto_mark        
    #json = make_json([car])
    return HttpResponse(json.dumps(carDetails))
    
    
    
    


def json_handler(request, getParam, paramValue1=None, paramValue2=None):
    if getParam == 'get_car_mark':
        return get_car_mark(request)
    if getParam == 'get_car_model_by_mark_id':
        if paramValue1:
            return get_car_model_by_mark_id(paramValue1)
    if getParam == 'get_goods_categories':
        return get_goods_categories(request)
    if getParam == 'get_engines_by_make_and_model':
        return get_engines_by_make_and_model(paramValue1, paramValue2)
    if getParam == 'get_user_car_details':
        return get_user_car_details(request)
        
    response = 'Func: {0}<br>Param1: {1}<br>Param2: {2}'.format(getParam,
                                                            paramValue1,
                                                            paramValue2)    
    return HttpResponse(response)


def make_json(iterable):
    return serializers.serialize("json", iterable)
    


def make_parts_table(partList, request, action='add'):
    if not partList:
        return 'No parts were found'
    tableString = '<table border="1" width="100%" align="center" class="bodytable">'
    tableFormat = ('<tr><td>{picture}</td><td>{part_name}</td>' +
                     '<td align="left">{part_details}</td>' +
                     '<td align="left">{availability}</td>' +
                     '<td>{price}</td>' +
                     '{favourites}' + 
                     '</tr>')
    
    tableDict = {'picture': '',
                 'part_name': 'Part name',
                 'part_details': 'Part details',
                 'availability': 'Availability',
                 'price': 'Price',
                 }
    if request.user.is_authenticated():
        tableDict['favourites'] = '<td>Add to favourites</td>'
    else:
        tableDict['favourites'] = ''
        
    tableString += tableFormat.format(**tableDict)   
    

    
    for i,part in enumerate(partList):
        # clear data
        for key in tableDict.keys():
            tableDict[key] = ''
            
        picture = ''
        if part.pilt.url:
            picture = '<img src="{}" />'.format(part.pilt.url)
        tableDict['picture'] = picture
        
        part_name = ''
        if part.artikli_nr:
            part_name = 'Article: {}'.format(part.artikli_nr)
            
        if part.varuosa_kategooria and part.varuosa_kategooria.nimetus:
            part_name += '<br>Category: {}'.format(part.varuosa_kategooria.nimetus)
            
        tableDict['part_name'] = part_name
        
        part_details = ''
        if part.tootja and part.tootja.nimetus:
            part_details = 'Manufacturer: {}'.format(part.tootja.nimetus)
        if part.katalogi_nr:
            part_details += '<br>Catalog nr: {}'.format(part.katalogi_nr)
        if part.monteerimis_koht:
            part_details += '<br>Assembly place: {}'.format(part.monteerimis_koht)
        if part.varuosa_kulg:
            part_details += '<br>Side: {}'.format(part.varuosa_kulg)   
        if part.mootmed:
            part_details += '<br>Dimension: {}'.format(part.mootmed)
        if part.kirjeldus:
            part_details += '<br>Description: {}'.format(part.kirjeldus)
        
        tableDict['part_details'] = part_details
        
        
        availability = ''
        if part.kogus:
            availability = 'Quantity: {}'.format(part.kogus)
        if part.varuosa_seisund and part.varuosa_seisund.nimetus:
            availability += '<br>Availability: {}'.format(part.varuosa_seisund.nimetus)
            
                    
        tableDict['availability'] = availability
        
        price = ''
        if part.tukihind:
            price = 'Price: {} EUR'.format(part.tukihind)
            
        tableDict['price'] = price
        
        favourites = ''
        if request.user.is_authenticated():            
            if action == 'add':
                imgTag = ('<img src="/static/shop/images/favourite_icon.png" width="20px" ' +
                          'onclick="addFavourite(event)" '+
                          'alt="Add to favourites" ' +
                          'title="Add to favourites" ' +                      
                          'id="varuosa_{0}" />').format(str(part.varuosa_id))
            else:
                imgTag = ('<img src="/static/shop/images/favourite_delete_icon.png" width="20px" ' +
                          'onclick="deleteFavourite(event)" '+
                          'alt="Delete from favourites" ' +
                          'title="Delete from favourites" ' +                      
                          'id="varuosa_{0}" />').format(str(part.varuosa_id))
            favourites = '<td>{}</td>'.format(imgTag)
            
        tableDict['favourites'] = favourites
        
        tableString += tableFormat.format(**tableDict)
    tableString +='</table>'
    return tableString
    

@request_type_required
def search_items(request):    
    partList = [] 
    try:   
        if request.POST['mark_id']:
            mark_id = int(request.POST['mark_id'])
        if request.POST['model_id']:
            model_id = int(request.POST['model_id'])
        if request.POST['category_id']:
            category_id = int(request.POST['category_id'])
        if request.POST['motor_id']:
            motor_id = int(request.POST['motor_id'])
            
        modifications = Auto_modifikatsioon.objects.filter(auto_mudel=model_id,
                                                       mootor = motor_id).values_list('auto_modifikatsioon_id', flat=True).order_by('auto_modifikatsioon_id')
        if not modifications:
            return HttpResponseServerError('No such models exist ')
        
        #modIds = [ mod.id for mod in modifications]
        
        varuosaList = Varuosa.objects.filter(auto_modifikatsioonid__auto_modifikatsioon_id__in=modifications)
        
        if not varuosaList:
            return HttpResponse('No parts found')
        
        for varuosa in varuosaList:            
            if category_id == 0:                
                partList.append(varuosa)
            else:                
                if varuosa.varuosa_kategooria.kood == category_id:
                    partList.append(varuosa)
                        
    except Exception as e:
        report = ''
        for key,value in request.POST.iteritems():
            if value:
                report += key + ' = ' + value + '\n'
            else:
                report += key + ' = ' + 'unknown\n'
        return HttpResponseServerError('\nWrong request data: \n ' + report)
    
    table = make_parts_table(partList, request)
    return HttpResponse(table)    

@login_required(login_url='/accounts/login/')
def show_user_parts(request):
    user = request.user
    # remake request
    request.method = 'POST'
    request.META['REQUEST_METHOD'] = 'POST'
    try:    
        klient = Klient.objects.get(user=request.user)
        car = klient.kliendi_auto
    except Klient.DoesNotExist:
        car = None
    
    if not ( car and        
        car.auto_mudel and
        car.mootor):
        message = 'Please  specify your car in profile section'
        return render_to_response('shop/shop_user_favourite_parts.html',
                               {'favTable': '',
                                'user': user,
                                'message': message})
        
        
    
    request.POST = {'mark_id': str(car.auto_mudel.auto_mark.auto_mark_id),
                    'model_id': str(car.auto_mudel.auto_mudel_id),
                    'category_id': str(0),
                    'motor_id': str(car.mootor.mootor_id)}
 
#    request.POST['mark_id'] = car.make
#    request.POST['model_id'] = car.model
#    request.POST['category_id'] = 0
#    request.POST['motor_id'] = car.engine
    
    partTable = search_items(request)   
    
    return render_to_response('shop/shop_user_favourite_parts.html',
                               {'favTable': partTable.content,
                                'user': user,
                                'message': ''})
    

@login_required(login_url='/accounts/login/')
def show_user_favourites(request):
    try:
        lemmikud = Lemmik_varuosa.objects.filter(kasutaja=request.user).all()
    except Lemmik_varuosa.DoesNotExist:
        lemmikud = None
    if lemmikud:
        varuosad = []
        for lemmik in lemmikud:
            varuosad.append(lemmik.varuosa)
        favTable = make_parts_table(varuosad, request, action='delete')
    else:
        favTable = 'You have not any favourite parts'     
            
    message = None
    if 'message' in request.GET.keys():
        message = request.GET['message']
        
    return render_to_response('shop/shop_user_favourite_parts.html',
                               {'favTable': favTable,
                                'user': request.user,
                                'message': message})

@login_required(login_url='/accounts/login/')
def show_user_profile(request):
    
    
    user = request.user
    
    message = ''
    initialData = {'username': user.username,
                       'first_name': user.first_name,
                       'last_name': user.last_name,
                       'email' : user.email,
                       }
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        
        if not request.user.username == form.data['username']:
            present = form.check_username_presense(form.data['username'])
            
        
        if form.is_valid():            
            if 'username' in form.data.keys() and form.data['username']:
                if not request.user.username == form.data['username']:
                    present = form.check_username_presense(form.data['username'])
                    if present:
                        message = ('<p style="color: red;">' + 
                                   '{0} username is already in use.<br>' +
                                   'Please choose another one</p>').format(form.data['username'])
                                   
                        return render_to_response('shop/shop_user_profile.html',
                                   {'user': request.user,
                                    'form': form,
                                    'message': message})
                              
                user.username = form.data['username']
            if 'first_name' in form.data.keys() and form.data['first_name']:
                user.first_name = form.data['first_name']
            if 'last_name' in form.data.keys() and form.data['last_name']:
                user.last_name = form.data['last_name']
            if 'email' in form.data.keys() and form.data['email']:
                user.email = form.data['email']
            
            if 'old_password' in form.data.keys() and form.data['old_password']:
                if request.user.check_password(form.data['old_password']):
                    if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                        request.user.set_password(form.cleaned_data['password1'])                        
                else:
                    message = ('<p style="color: red;">' + 
                               '{0}, your password is incorrect<br>' +
                               'Please give correct old password</p>').format(user.username)
                                   
                    return render_to_response('shop/shop_user_profile.html',
                               {'user': request.user,
                                'form': form,
                                'message': message}) 
            
            if( 'make' in form.data.keys() and form.data['make'] and
                'model' in form.data.keys() and form.data['model'] and
                'engine' in form.data.keys() and form.data['engine'] and
                int(form.data['make']) != 0 and
                int(form.data['model']) != 0 and
                int(form.data['engine']) != 0  ):
                make_id = int(form.data['make'])
                model_id = int(form.data['model'])
                engine_id = int(form.data['engine'])
                
                make, model, engine = CustomShopBackend().get_car_details(make_id,
                                                                        model_id,
                                                                        engine_id)
                if not CustomShopBackend().save_user_car(make, model, engine, user):
                    message = '<p style="color: red;"> Please specify your car (make, model, engine)</p>'
                    
            else:
                message = '<p style="color: red;"> Please specify your car (make, model, engine)</p>'
        else:
            return render_to_response('shop/shop_user_profile.html',
                               {'user': request.user,
                                'form': form,
                                'message': message})
            
        
        user.save()
        
        initialData = {'username': user.username,
                       'first_name': user.first_name,
                       'last_name': user.last_name,
                       'email' : user.email,                       
                       }
        
        form = UserProfileForm(initial=initialData) 
        
    else:
        form = UserProfileForm(initial=initialData)
    return render_to_response('shop/shop_user_profile.html',
                               {'favTable': 'here would be user profile',
                                'user': request.user,
                                'form': form,
                                'message': message})
        



@login_required(login_url='/accounts/login/')
@request_type_required
def add_part_to_favourites(request, partId):
    if partId:
        varuosaId = str(partId)
        varuosa = Varuosa.objects.get(varuosa_id=varuosaId)
        if not varuosa:
            return HttpResponseServerError('\nWrong part id: \n ' + partId +
                                           '\n Such part is not found')
        try:
            klient = User.objects.get(id=request.user.id)
            lemmik = Lemmik_varuosa.objects.get(kasutaja=klient,
                                                varuosa=varuosa)
        except Lemmik_varuosa.DoesNotExist:
            lemmik = None
        if lemmik:            
            responseText = ('Varuosa: {0} \n' + 
                'is already in your favourite list').format(varuosa.katalogi_nr)                   
            return  HttpResponse(responseText)               
           
        else:
            lemmik = Lemmik_varuosa()
            klient = Klient.objects.get(user=request.user)             
            lemmik.kasutaja = klient            
            lemmik.varuosa = varuosa
            lemmik.save()           
    responseText = 'Varuosa: {0} \nis added to your favourite list'.format(varuosa.katalogi_nr)       
    return  HttpResponse(responseText)   

@login_required(login_url='/accounts/login/')
@request_type_required
def delete_part_from_favourites(request, partId):
    if partId:
        varuosaId = str(partId)
        varuosa = Varuosa.objects.get(varuosa_id=varuosaId)
        if not varuosa:
            return HttpResponseServerError('\nWrong part id: \n ' + partId +
                                           '\n Such part is not found')
        try:
            klient = User.objects.get(id=request.user.id)
            lemmik = Lemmik_varuosa.objects.get(kasutaja=klient,
                                                varuosa=varuosa)
        except Lemmik_varuosa.DoesNotExist:
            lemmik = None
        if lemmik: 
            lemmik.delete()
        else:
            return HttpResponseServerError('\nNothing to delete. You have no favourites')
                            
    responseText = 'Varuosa: {0} \nwas removed from your favourite list'.format(varuosa.katalogi_nr)       
    return  HttpResponseRedirect('/shop/favourites/?message={0}'.format(responseText))

# database-storage view
# is needed to display images from db
def image_view(request, filename):
    # Read file from database
    storage = DatabaseStorage(options=settings.DBS_OPTIONS)
    image_file = storage.open(filename, 'rb')
    if not image_file:
        raise Http404
    file_content = image_file.read()
    
    # Prepare response
    content_type, content_encoding = mimetypes.guess_type(filename)
    response = HttpResponse(content=file_content, mimetype=content_type)
    response['Content-Disposition'] = 'inline; filename=%s' % filename
    if content_encoding:
        response['Content-Encoding'] = content_encoding
    return response