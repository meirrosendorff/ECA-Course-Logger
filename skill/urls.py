from django.conf.urls import url

from . import views

app_name = 'skill'
urlpatterns = [
    url(r'skillLog/$', views.skillLogView.as_view(), name='skillLog'),
]
