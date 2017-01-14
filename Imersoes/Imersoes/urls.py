"""
Definition of urls for Imersoes.
"""

from django.conf.urls import include, url
from Feedbacks import views


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', Imersoes.views.home, name='home'),
    # url(r'^Imersoes/', include('Imersoes.Imersoes.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view),
    url(r'^logout/$', views.logout),
    url(r'^loggedin/$', views.loggedin),
    url(r'^invalid$', views.invalid_login),
    url(r'^Psicologo$', views.Psicologo_view),
    url(r'^Psicologo/novo_cliente/$', views.novo_cliente_view),
    url(r'^Cliente/(?P<WebKey>[0-9a-z-]+)$', views.cliente_view, name = 'cliente' ),
    url(r'^Cliente/sucesso/$', views.sucesso),
    url(r'^Indicado/(?P<WebKey>[0-9a-z-]+)$', views.indicado_view, name = 'indicado' ),
]


