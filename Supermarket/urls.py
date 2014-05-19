from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from django.contrib import admin
admin.autodiscover()

from Supermarket import views

urlpatterns = patterns('',
    url(r'^$', views.login, name = 'login'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^logout$', views.logout, name = 'logout'),
    url(r'^logged_out$', views.logged_out, name = 'logged_out'),
    url(r'^invalidLogin$', views.invalidLogin, name = 'invalidLogin'),
    url(r'^checkCreds$', views.checkCreds, name = 'checkCreds'),
    url(r'^salesClerk$', views.salesClerk, name = 'salesClerk'),
    url(r'^employee$', views.employee, name = 'employee'),
    url(r'^manager$', views.manager, name = 'manager'),
    url(r'^newUser$', views.newUser, name = 'newUser'),
    url(r'^newUserReg$', csrf_exempt(views.newUserReg), name = 'newUserReg'),
    url(r'^searchItem$', csrf_exempt(views.searchItem), name = 'searchItem'),
    url(r'^changePrice$', csrf_exempt(views.changePrice), name = 'changePrice'),
    url(r'^toptop$', csrf_exempt(views.toptop), name = 'toptop'),
    url(r'^newItem$', csrf_exempt(views.newItem), name = 'newItem'),
    url(r'^newSItem$', csrf_exempt(views.newSItem), name = 'newSItem'),
    url(r'^regItem$', csrf_exempt(views.regItem), name = 'regItem'),
    url(r'^updateRecords$', csrf_exempt(views.updateRecords), name = 'updateRecords'),
    url(r'^getStats$', csrf_exempt(views.getStats), name = 'getStats'),
    url(r'^itemInfo/(?P<item_id>\d+)/$', csrf_exempt(views.itemInfo), name = 'itemInfo'),
    url(r'^admin/', include(admin.site.urls)),
)
