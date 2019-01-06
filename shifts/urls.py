from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'booking/(?P<bookingType>\w{0,50})/$', bookingView, name='booking'),
    url(r'booking/$', bookingGlobalView, name='bookingGlobal'),
    url(r'myShifts/$', myShiftsView, name='myShifts'),
    url(r'remove/$', removeShift, name='remove'),
]