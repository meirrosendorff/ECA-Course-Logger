from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'login/$', views.loginView.as_view(), name='login'),
    url(r'logout/$', views.logoutView.as_view(), name='logout'),
]
