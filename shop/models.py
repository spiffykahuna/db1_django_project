from django.db import models
from numpy.lib.arraysetops import unique
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import User
from django.db.models.aggregates import Max

from database_storage import DatabaseStorage
from db1_django_project import settings
from django.db.models.loading import get_model





# Create your models here.

class Klassifikaator(models.Model):
    kood = models.PositiveIntegerField(primary_key=True)         
    nimetus = models.CharField(max_length=30, unique=True)
    kirjeldus = models.CharField(max_length=100, null=True)    

    def __unicode__(self):
        return self.nimetus
    
    class Meta:
        ordering = ['nimetus']        
        abstract = True

def next_auto_mark_id():
    if Auto_mark.objects.count():    
        max_id = Auto_mark.objects.aggregate(Max('auto_mark_id'))
        return str(int(max_id['auto_mark_id__max']) + 1)
    else:
        return 1
    
class Auto_mark(models.Model):
    auto_mark_id = models.PositiveSmallIntegerField(primary_key=True,
                                                    default=next_auto_mark_id)
    mark = models.CharField(max_length=30, unique=True)
    
    def __unicode__(self):
        return self.mark
    
    class Meta:
        ordering = ['mark']
        verbose_name_plural = "auto margid"
        

def next_mootor_id():
    if Mootor.objects.count():    
        max_id = Mootor.objects.aggregate(Max('mootor_id'))
        return str(int(max_id['mootor_id__max']) + 1)
    else:
        return 1 
    
class Mootor(models.Model):
    KYTUS_CHOICES = (
        (u'B', u'Bensiin'),
        (u'D', u'Diisel'),
        (u'G', u'Gaas'),
        (u'E', u'Elekter'),
        (u'B_E', u'Bensiin/Elekter'),
        (u'B_G', u'Bensiin/Gaas'),
        (u'O', u'Teine'),
    )
    mootor_id = models.PositiveIntegerField(primary_key=True,
                                            default=next_mootor_id)         
    nimetus = models.CharField(max_length=100)
    kirjeldus = models.CharField(max_length=255, null=True, blank=True)    
    motor_code_tip = u'Engine code'
    mootori_tyyp = models.CharField(max_length=100, help_text=motor_code_tip,)
    kytus = models.CharField(max_length=30, choices=KYTUS_CHOICES, default='B')
    kubatuur_cm3 = models.PositiveSmallIntegerField()
    voimsus_kw = models.PositiveSmallIntegerField()
    silindrite_arv = models.PositiveSmallIntegerField(default=4)
    
    def __unicode__(self):
        return self.nimetus + ' ' + str(self.voimsus_kw) + ' kW ' + self.mootori_tyyp
    
    class Meta:
        ordering = ['nimetus']
        verbose_name_plural = "mootorid"
        unique_together = (("nimetus",
                            "mootori_tyyp",
                            "kytus",
                            "kubatuur_cm3",
                            "voimsus_kw",
                            "silindrite_arv"),
                           )

def next_auto_mudel_id():
    if Auto_mudel.objects.count():    
        max_id = Auto_mudel.objects.aggregate(Max('auto_mudel_id'))
        return str(int(max_id['auto_mudel_id__max']) + 1)
    else:
        return 1    
        
class Auto_mudel(models.Model):
    auto_mudel_id = models.PositiveIntegerField(primary_key=True,
                                                default=next_auto_mudel_id)  
    auto_mark = models.ForeignKey(Auto_mark)           
    mudel = models.CharField(max_length=100)
    mootorid = models.ManyToManyField(Mootor, through='Auto_modifikatsioon')    
    valjalaske_algus = models.DateField(null=True)
    valjalaske_lopp = models.DateField(null=True)
    
    
    
    def __unicode__(self):
        return self.mudel
    
    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        try:
            self.clean()
        except ValidationError:
            raise
        # Call the "real" save() method.s
        super(Auto_mudel, self).save(*args, **kwargs)
    
    def clean(self):
        from django.core.exceptions import ValidationError
                
        if self.valjalaske_lopp < self.valjalaske_algus:
            raise ValidationError('Start date should be smaller than end date')
    
    class Meta:
        ordering = ['mudel']
        unique_together = (("auto_mark", "mudel"),)
        verbose_name_plural = "auto mudelid"        
           




def next_auto_modifikatsioon_id():
    if Auto_modifikatsioon.objects.count():    
        max_id = Auto_modifikatsioon.objects.aggregate(Max('auto_modifikatsioon_id'))
        return str(int(max_id['auto_modifikatsioon_id__max']) + 1)
    else:
        return 1    
        
        
class Auto_modifikatsioon(models.Model):
    auto_modifikatsioon_id = models.PositiveIntegerField(primary_key=True,
                                                         default=next_auto_modifikatsioon_id)    
    auto_mudel = models.ForeignKey(Auto_mudel)
    mootor = ChainedForeignKey(
        Mootor, 
        chained_field="auto_mudel",
        chained_model_field="auto_mudel", 
        show_all=True, 
        auto_choose=True
    ) 
    
    unicodeNimi = models.CharField(max_length=255, null=True, blank=True)
    
    
    
    def tee_unicodeNimi(self):
        result = ''
        if self.auto_mudel.auto_mark and self.auto_mudel.auto_mark.__unicode__():
            result += self.auto_mudel.auto_mark.__unicode__() 
        if self.auto_mudel and self.auto_mudel.__unicode__():
            result += ' ' + self.auto_mudel.__unicode__()            
        if self.mootor and self.mootor.__unicode__():
            result += ' ' + self.mootor.__unicode__()
        
        return result 
    
    
    def __unicode__(self):
        if self.unicodeNimi:
            return self.unicodeNimi
        else:
            self.unicodeNimi = self.tee_unicodeNimi()
            self.save()
            return self.unicodeNimi 
        
    def save(self, *args, **kwargs):
        self.unicodeNimi = self.tee_unicodeNimi()
        # Call the "real" save() method.s
        super(Auto_modifikatsioon, self).save(*args, **kwargs) 
        
    class Meta:
        ordering = ['auto_mudel__auto_mark', 'auto_mudel']
        verbose_name_plural = "Auto modifikatsioonid"
        unique_together = (("auto_mudel", "mootor"),)  
           
    
def next_varusa_kategooria_kood():
    if Varuosa_kategooria.objects.count():    
        max_id = Varuosa_kategooria.objects.aggregate(Max('kood'))
        return str(int(max_id['kood__max']) + 1)
    else:
        return 1       

class Varuosa_kategooria(Klassifikaator):
    """
        There should be categories for the goods
    """
    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        self.kood = int( next_varusa_kategooria_kood())
        try:
            self.clean()
        except ValidationError:
            raise
        # Call the "real" save() method.s
        
        super(Varuosa_kategooria, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['nimetus']        
        verbose_name_plural = "Varuosade kategooriad"    

def next_varusa_seisund_kood():    
    if Varuosa_seisund.objects.count():    
        max_id = Varuosa_seisund.objects.aggregate(Max('kood'))
        return str(int(max_id['kood__max']) + 1)
    else:
        return 1  
    

class Varuosa_seisund(Klassifikaator):
    """
        There should be categories for the goods
    """
    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        self.kood = int( next_varusa_seisund_kood())
        try:
            self.clean()
        except ValidationError:
            raise
        # Call the "real" save() method.s
        
        super(Varuosa_seisund, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['nimetus']        
        verbose_name_plural = "Varuosade seisud"

def next_varusa_kulg_kood():    
    if Varuosa_kulg.objects.count():    
        max_id = Varuosa_kulg.objects.aggregate(Max('kood'))
        return str(int(max_id['kood__max']) + 1)
    else:
        return 1  

class Varuosa_kulg(Klassifikaator):
    
    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        self.kood = int( next_varusa_kulg_kood())
        try:
            self.clean()
        except ValidationError:
            raise
        # Call the "real" save() method.s
        
        super(Varuosa_kulg, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['nimetus']
        verbose_name_plural = "Varuosa kuljed"



def next_tootja_id():
    if Tootja.objects.count():
        max_id = Tootja.objects.aggregate(Max('tootja_id'))
        return str(int(max_id['tootja_id__max']) + 1)
    else:
        return 1        

class Tootja(models.Model):    
    tootja_id = models.PositiveSmallIntegerField(primary_key=True,
                                                 default=next_tootja_id)      
    nimetus = models.CharField(max_length=30, unique=True)
    kirjeldus = models.CharField(max_length=100, null=True)
    
    lehekulg = models.URLField(null=True, blank=True)
    telefon = models.CharField(max_length=20, null=True, blank=True)    
    email = models.EmailField(null=True, blank=True)
    aadress = models.CharField(max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        return self.nimetus
    
    class Meta:
        ordering = ['nimetus']
        verbose_name_plural = "Tootjad"
        

    

def next_artikli_nr():
    if Varuosa.objects.count():
        max_id = Varuosa.objects.aggregate(Max('varuosa_id'))
        newNumber = int(max_id['varuosa_id__max']) + 1
        return 'ALM-{0}'.format(newNumber)
    else:
        return 'ALM-1'


def next_varuosa_id():
    if Varuosa.objects.count():    
        max_id = Varuosa.objects.aggregate(Max('varuosa_id'))
        return str(int(max_id['varuosa_id__max']) + 1)
    else:
        return 1


class Varuosa(models.Model):
    varuosa_id = models.PositiveIntegerField(primary_key=True,
                                             default=next_varuosa_id)
    artikli_nr = models.CharField(max_length=50, unique=True, default=next_artikli_nr)
    tukihind = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    kogus = models.PositiveSmallIntegerField(default=0)    
    katalogi_nr = models.CharField(max_length=50, blank=True, null=True)
    monteerimis_koht = models.CharField(max_length=100, blank=True, null=True)    
    mootmed = models.CharField(max_length=50, blank=True, null=True)
    kirjeldus = models.TextField(blank=True, null=True)
       
       
    varuosa_kategooria = models.ForeignKey(Varuosa_kategooria)
    varuosa_kulg = models.ForeignKey(Varuosa_kulg, blank=True, null=True)
    varuosa_seisund = models.ForeignKey(Varuosa_seisund, default=1)
    tootja = models.ForeignKey(Tootja)
    
    auto_modifikatsioonid = models.ManyToManyField(Auto_modifikatsioon)
    
    pilt = models.ImageField(
            null=True,
            blank=True,
            upload_to='img_varuosad/',            
            storage=DatabaseStorage(options=settings.DBS_OPTIONS),
            default = 'img_varuosad/default_varuosa.png'                       
        )
    
    def __unicode__(self):
        return self.artikli_nr
    
    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        try:
            self.clean()
        except ValidationError:
            raise
        # Call the "real" save() method.s
        super(Varuosa, self).save(*args, **kwargs)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        import re
        # Don't allow draft entries to have a pub_date.
        pattern = re.compile('^ALM-[\d]+[a-zA-Z]*')
        if not pattern.match(self.artikli_nr):
            raise ValidationError('Artikli nr. should be like ALM-x, where x is any digit')
        if self.tukihind < 0:
            raise ValidationError('Tukihind should be positive number')        
    
    class Meta:
        ordering = ['artikli_nr']
        unique_together = (("artikli_nr", "varuosa_kategooria"),)
        verbose_name_plural = "varuosad"
 

#def next_varuosa_sobivus_id():
#    if Varuosa_sobivus.objects.count():
#        max_id = Varuosa_sobivus.objects.aggregate(Max('varuosa_sobivus_id'))
#        return str(int(max_id['varuosa_sobivus_id__max']) + 1)
#    else:
#        return 1


#class Varuosa_sobivus(models.Model):
#    auto_mark = models.ForeignKey(Auto_mark)     
#    auto_mudel = ChainedForeignKey(
#        Auto_mudel, 
#        chained_field="auto_mark",
#        chained_model_field="auto_mark", 
#        show_all=False, 
#        auto_choose=True
#    )
#    mootor = ChainedForeignKey(
#        Mootor, 
#        chained_field="auto_mudel",
#        chained_model_field="auto_mudel", 
#        show_all=True, 
#        auto_choose=True
#    ) 
#    
#    
#    varuosa = models.ManyToManyField(Varuosa)
#    varuosa_sobivus_id = models.PositiveIntegerField(primary_key=True,
#                                                     default=next_varuosa_sobivus_id)
#    varuosa = models.OneToOneField(Varuosa, related_name='sobivus')
#    modifikatsioon = models.ManyToManyField(Auto_modifikatsioon)
#    
#    def __unicode__(self):
#        result = self.varuosa.artikli_nr
#        if self.modifikatsioon.all():
#            ids = [mod.auto_modifikatsioon_id for mod in self.modifikatsioon.all()]
#            result +=  ' ' + str(ids)
#        else:
#            result +=  ' ' + str([])
#        return result    
#
#    class Meta:
#        ordering = ['varuosa']
#        verbose_name_plural = "Varuosade sobivused"
#        #unique_together = (("varuosa", "modifikatsioon"),)    

class Klient(User):
    lemmikud_varuosad = models.ManyToManyField(Varuosa, through='Lemmik_varuosa')
    user = models.OneToOneField(User, unique=True)
    kliendi_auto = models.ForeignKey(Auto_modifikatsioon, blank=True, null=True)
    #user =  models.OneToOneField(User, parent_link=True)
    #class Meta:
        #abstract = True
        

def next_lemmik_varuosa_id():
    if Lemmik_varuosa.objects.count():
        max_id = Lemmik_varuosa.objects.aggregate(Max('lemmik_varuosa_id'))
        return str(int(max_id['lemmik_varuosa_id__max']) + 1)
    else:
        return 1


class Lemmik_varuosa(models.Model):
    lemmik_varuosa_id = models.PositiveIntegerField(primary_key=True,
                                                    default=next_lemmik_varuosa_id)
    kasutaja = models.ForeignKey(Klient)
    varuosa = models.ForeignKey(Varuosa)
    
    class Meta:
        verbose_name_plural = "Lemmikud varuosad"
        unique_together = ('kasutaja', 'varuosa')
    

#class Kliendi_auto(models.Model):
#    """
#        User car  will  be stored here
#    """   
#    
#    kliendi_auto_id = models.PositiveIntegerField(primary_key=True)
#    
#    auto_mark = models.ForeignKey(Auto_mark, null=False)     
#    auto_mudel = ChainedForeignKey(
#        Auto_mudel, 
#        chained_field="auto_mark",
#        chained_model_field="auto_mark", 
#        show_all=False, 
#        auto_choose=True,
#        null=False
#    )
#    mootor = ChainedForeignKey(
#        Mootor, 
#        chained_field="auto_mudel",
#        chained_model_field="auto_mudel", 
#        show_all=True, 
#        auto_choose=True,
#        null=False
#    ) 
#    
#    def __unicode__(self):
#        uni = u''
#        if self.auto_mark and self.model and self.mootor:
#            #uni = (self.kasutaja.__unicode__() + ' ' +
#            uni = (self.auto_mark.__unicode__() + ' ' +
#                self.model.__unicode__() + ' ' + 
#                self.mootor.__unicode__())       
#        return uni
#                 
#                 
#    class Meta:
#        ordering = ['auto_mark', 'auto_mudel', 'mootor']
#        verbose_name_plural = "Kliendi autod"
#        unique_together = (("auto_mark", "auto_mudel", "mootor"),)

   
    
    