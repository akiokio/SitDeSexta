from django.conf.urls import patterns, include, url

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SitDeSextaReloaded.views.home', name='home'),
    # url(r'^SitDeSextaReloaded/', include('SitDeSextaReloaded.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^admin/', include(admin.site.urls)),

    #    comments module
    url(r'^comments/', include('django.contrib.comments.urls')),

    #My Urls
    url(r'^$', 'Ranking.views.landing_page'),
    url(r'^index/$','Ranking.views.index'),
    url(r'^contato','Ranking.views.contato'),

    (r'^static/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^tournaments/(?P<tournament_id>\d+)$' , 'Ranking.views.tournament'),
    url(r'^tournaments', 'Ranking.views.tournaments'),

    url(r'^news/(?P<news_id>\d+)$', 'Ranking.views.news'),
    (r'^accounts/', include('userena.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))