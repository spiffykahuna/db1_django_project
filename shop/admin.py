#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Apr 6, 2012

@author: deko
'''

from django.contrib import admin
from models import Auto_mark, Auto_mudel, Mootor, Auto_modifikatsioon
from models import Varuosa
from models import Lemmik_varuosa
#from models import Kliendi_auto
from models import Tootja
from models import Varuosa_kategooria
from models import Varuosa_seisund
from models import Varuosa_kulg


#from db1_django_project.books.models import Publisher, Author, Book

class Auto_markAdmin(admin.ModelAdmin):
    exclude = ('auto_mark_id',)

class Auto_mudelAdmin(admin.ModelAdmin):
    list_display = ('auto_mudel_id',
                    'auto_mark',
                    'mudel',                    
                    'valjalaske_algus',
                    'valjalaske_lopp')
    exclude = ('auto_mudel_id',)
    list_filter = ('auto_mark',)
    date_hierarchy = 'valjalaske_algus'
    ordering = ('auto_mark', 'mudel',)
    filter_horizontal = ('mootorid',) 
    search_fields = ('auto_mark__mark',
                     'mudel',
                     'auto_mudel_id',) 


class MootorAdmin(admin.ModelAdmin):
    list_display = ('mootor_id',
                    'nimetus',
                    'mootori_tyyp',                    
                    'kytus',
                    'kubatuur_cm3',
                    'voimsus_kw',
                    'silindrite_arv')
    
    fields = (      'nimetus',
                    'mootori_tyyp',                    
                    'kytus',
                    'kubatuur_cm3',
                    'voimsus_kw',
                    'silindrite_arv',
                    'kirjeldus')
    #list_filter = ('nimetus', 'mootori_tyyp',)
    search_fields = ('mootor_id',
                     'nimetus',
                     'mootori_tyyp')


class Auto_modifikatsioonAdmin(admin.ModelAdmin):
    list_display = ('auto_modifikatsioon_id',
                    'get_auto_mark',                    
                    'auto_mudel',                    
                    'mootor',)
    fields = ('auto_mudel', 'mootor',)
    list_filter = ('auto_mudel','mootor')
    search_fields = ('auto_mudel__auto_mark__mark',
                     'auto_mudel__mudel',
                     'mootor__nimetus',
                     'auto_modifikatsioon_id')
    ordering = ('auto_mudel__auto_mark', 'auto_mudel',)
    list_select_related = True
    raw_id_fields = ("auto_mudel", "mootor")
    
    def get_auto_mark(self, obj):
        return obj.auto_mudel.auto_mark
    get_auto_mark.short_description = 'Auto mark'   

    
#class Kliendi_autoAdmin(admin.ModelAdmin):
#    fieds = ('kasutaja', 'auto_mark','auto_mudel', 'mootor')
#    list_display = ('kasutaja',
#                    'auto_mark',
#                    'auto_mudel',                    
#                    )
#    list_filter = ('auto_mark', 'auto_mudel',)
#    search_fields = ('auto_mark__mark',
#                     'auto_mudel__mudel',
#                     'mootor__nimetus',
#                     'kasutaja__username',
#                     'kasutaja__first_name',
#                     'kasutaja__last_name',
#                     'kasutaja__email')
#    ordering = ('kasutaja', 'auto_mark','auto_mudel',)
#    list_select_related = True

#class Varuosa_sobivusInline(admin.TabularInline):
#    model =  Varuosa_sobivus
#    raw_id_fields = ("modifikatsioon",)

class VaruosaAdmin(admin.ModelAdmin):
    fields = (#'varuosa_id',
              'artikli_nr',
              'tukihind',
              'kogus',
              'varuosa_seisund',
              'tootja',
              'varuosa_kategooria',
              'katalogi_nr',
              'monteerimis_koht',
              'varuosa_kulg',
              'mootmed',
              'pilt',
              'auto_modifikatsioonid'
              )
    list_display = ('artikli_nr',
                    'varuosa_kategooria',
                    'tootja',
                    'tukihind',
                    'kogus',
                    'varuosa_seisund')
    raw_id_fields = ('auto_modifikatsioonid',)
    #inlines = [ Varuosa_sobivusInline,]

#def varuosa_list(obj):varuosa_sobivus_id
#        result = ''
#        varuosad = obj.varuosa.all()
#        
#        for varuosa in varuosad:
#            result += varuosa.__unicode__()
#            result += '<br>'
#        return result
#varuosa_list.allow_tags = True
#varuosa_list.short_description = 'Varuosa Nimetused'
#
def modifikatsioon_list(obj):
    result = ''
    mods = obj.modifikatsioon.all()
    for mod in mods:
        result += mod.__unicode__()
        result += '<br>'
    return result
modifikatsioon_list.allow_tags = True
modifikatsioon_list.short_description = 'Varuosa on sobiv autodele:'
        
        
#class Varuosa_sobivusAdmin(admin.ModelAdmin):
#    fields = ('varuosa', 'auto_mark', 'auto_mudel', 'mootor',)
#    #fields = ('varuosa', 'mootori_omamised',)
#    filter_horizontal = ('varuosa',)
#    search_fields = ('varuosa__katalogi_nr',
#                     'varuosa__artikli_nr',
#                     'auto_mark__mark',
#                     'auto_mudel__mudel',
#                     'mootor__mootori_tyyp')
#    #list_select_related = True
#    list_display = (varuosa_list, 'auto_mark', 'auto_mudel', 'mootor')
     #filter_horizontal = ('modification',)
#     fields = ('varuosa',
#               'modifikatsioon')
#     list_display = ('varuosa',
#               'modifikatsioon')
#     search_fields = ('varuosa__katalogi_nr',
#                     'varuosa__artikli_nr',
#                     'modifikatsioon__auto_mark__mark',
#                     'modifikatsioon__auto_mudel__mudel',
#                     'modifikatsioon__mootor__mootori_tyyp',
#                     'modifikatsioon__mootor__nimetus')
#     
#     list_display = ('varuosa', modifikatsioon_list,)
#     raw_id_fields = ("modifikatsioon",)
     
    

class Lemmik_varuosaAdmin(admin.ModelAdmin):
    fields = ('kasutaja', 'varuosa',)
    #fields = ('varuosa', 'mootori_omamised',)
    #filter_horizontal = ('varuosa',)
    search_fields = ('kasutaja__username',
                     'kasutaja__first_name',
                     'kasutaja__last_name',
                     'varuosa__katalogi_nr',
                     'varuosa__artikli_nr')
    #list_select_related = True
    list_display = ('kasutaja', 'varuosa',)

class TootjaAdmin(admin.ModelAdmin):
    exclude = ('tootja_id',)

class Varuosa_kulgAdmin(admin.ModelAdmin):
    exclude = ('kood',)

admin.site.register(Auto_mark,Auto_markAdmin)
admin.site.register(Auto_mudel, Auto_mudelAdmin)
admin.site.register(Mootor, MootorAdmin)
admin.site.register(Auto_modifikatsioon, Auto_modifikatsioonAdmin)
admin.site.register(Varuosa, VaruosaAdmin)
#admin.site.register(Varuosa_sobivus, Varuosa_sobivusAdmin)
admin.site.register(Lemmik_varuosa, Lemmik_varuosaAdmin)
#admin.site.register(Kliendi_auto, Kliendi_autoAdmin)
admin.site.register(Tootja, TootjaAdmin)
admin.site.register(Varuosa_kategooria,Varuosa_kulgAdmin)
admin.site.register(Varuosa_seisund, Varuosa_kulgAdmin)
admin.site.register(Varuosa_kulg, Varuosa_kulgAdmin)


