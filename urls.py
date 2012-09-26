from django.conf import settings
from django.conf.urls.defaults import *

from views import *

from books import views as books_views
from contact import views as contact_view

from books.views import about_pages
from django.views.generic.simple import direct_to_template


from django.views.generic import list_detail
from books.models import Publisher
from books.models import Book

from books.views import author_detail



# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
# Example:
    # (r'^myDjangoStudying/', include('myDjangoStudying.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),


from django.contrib import admin
from django.conf import settings
from db1_django_project.shop.views import image_view
admin.autodiscover()

publisher_info = {
    'queryset': Publisher.objects.all(),
    'template_name': 'publisher_list_page.html',
    'template_object_name': 'publisher',
}

book_info = {
    'queryset': Book.objects.order_by('-publication_date'),
}

urlpatterns = patterns('',                       
    (r'^admin/', include(admin.site.urls)),
    (r'^about/$', direct_to_template, {
                                       'template': 'about.html'
                                       }
     ),
    (r'^about/(\w+)/$', about_pages),
    (r'^publishers/$', list_detail.object_list, publisher_info),
    (r'^books/$', list_detail.object_list, book_info),
    (r'^authors/(?P<author_id>\d+)/$', author_detail),
    (r'^register/$', register),
    # registration
    (r'^accounts/', include('registration.backends.custom.urls')),    
    (r'^$', direct_to_template,
            { 'template': 'index.html' }, 'index'),
                       
    # database-storage images
    (r'^templates/shop/images/(?P<filename>[a-zA-Z0-9_@./]+)$', image_view),
    
    # static files
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    # contact form
    (r'^contact/', include('django_apps.contact_form.urls')),
    # smart select for select boxes
    (r'^chaining/', include('smart_selects.urls')),
    # parts shop
    (r'^shop/', include('shop.urls')),
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^debuginfo/$', debug),
    )
